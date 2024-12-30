#
# Copyright (C) 2024 Kian Cross
#

import secrets

from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import resolve, reverse
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _
from pretix.base.middleware import _merge_csp, _parse_csp, _render_csp
from pretix.control.signals import nav_event_settings
from pretix.presale.cookies import CookieProvider, UsageClass
from pretix.presale.signals import (
    html_head,
    process_response,
    register_cookie_providers,
)


def _get_google_analytics_measurements_id(event):
    return escape(event.settings.get("tracking_scripts_google_analytics") or "") or None


def _get_meta_pixel_dataset_id(event):
    return escape(event.settings.get("tracking_scripts_meta_pixel") or "") or None


@receiver(nav_event_settings, dispatch_uid="tracking_scripts_nav_event_settings")
def navbar_event_settings(sender, request, **kwargs):
    url = resolve(request.path_info)
    return [
        {
            "label": _("Tracking Scripts"),
            "url": reverse(
                "plugins:pretix_tracking_scripts:settings",
                kwargs={
                    "event": request.event.slug,
                    "organizer": request.organizer.slug,
                },
            ),
            "active": url.namespace == "plugins:pretix_tracking_scripts"
            and url.url_name == "settings",
        }
    ]


@receiver(
    register_cookie_providers, dispatch_uid="tracking_scripts_register_cookie_providers"
)
def register_cookie_providers_signal(sender, **kwargs):
    cookie_providers = []

    if _get_google_analytics_measurements_id(sender):
        cookie_providers.append(
            CookieProvider(
                identifier="tracking_scripts_google_analytics",
                provider_name="Google Analytics",
                usage_classes=[UsageClass.ANALYTICS],
                privacy_url="https://policies.google.com/technologies/partner-sites",
            )
        )

    if _get_meta_pixel_dataset_id(sender):
        cookie_providers.append(
            CookieProvider(
                identifier="tracking_scripts_meta_pixel",
                provider_name="Meta Pixel",
                usage_classes=[UsageClass.MARKETING],
            )
        )

    return cookie_providers


@receiver(html_head, dispatch_uid="tracking_scripts_html_head")
def html_head_signal(sender, request, **kwargs):
    header_content = []

    request.tracking_scripts_nonce = secrets.token_urlsafe()
    measurements_id = _get_google_analytics_measurements_id(sender)

    if measurements_id:
        request.tracking_scripts_output_content = True
        header_content.append(
            render_to_string(
                "pretix_tracking_scripts/google_analytics.html",
                {
                    "nonce": request.tracking_scripts_nonce,
                    "measurements_id": measurements_id,
                },
            )
        )

    dataset_id = _get_meta_pixel_dataset_id(sender)

    if dataset_id:
        request.tracking_scripts_output_content = True
        header_content.append(
            render_to_string(
                "pretix_tracking_scripts/meta_pixel.html",
                {"nonce": request.tracking_scripts_nonce, "dataset_id": dataset_id},
            )
        )

    return "\n".join(header_content)


@receiver(process_response, dispatch_uid="tracking_scripts_process_response")
def process_response_signal(sender, request, response, **kwargs):
    if not getattr(request, "tracking_scripts_output_content", None):
        return response

    if "Content-Security-Policy" in response:
        headers = _parse_csp(response["Content-Security-Policy"])
    else:
        headers = {}

    _merge_csp(
        headers,
        {
            "script-src": [f"'nonce-{request.tracking_scripts_nonce}'"],
            "style-src": [f"'nonce-{request.tracking_scripts_nonce}'"],
        },
    )

    if _get_google_analytics_measurements_id(sender):
        _merge_csp(
            headers,
            {
                "connect-src": [
                    "https://*.google-analytics.com",
                    "https://*.analytics.google.com",
                    "www.googletagmanager.com",
                ],
                "img-src": [
                    "https://*.google-analytics.com",
                    "www.googletagmanager.com",
                ],
            },
        )

    if _get_meta_pixel_dataset_id(sender):
        _merge_csp(
            headers,
            {
                "script-src": ["https://connect.facebook.net"],
                "connect-src": ["https://www.facebook.com/tr/"],
                "img-src": ["https://www.facebook.com"],
            },
        )

    if headers:
        response["Content-Security-Policy"] = _render_csp(headers)

    return response
