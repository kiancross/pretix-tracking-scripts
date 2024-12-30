#
# Copyright (C) 2024 Kian Cross
#

from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from pretix.base.forms import SettingsForm
from pretix.base.models import Event
from pretix.control.views.event import EventSettingsFormView, EventSettingsViewMixin


class TrackingScriptsSettingsForm(SettingsForm):
    tracking_scripts_google_analytics = forms.CharField(
        label=_("Google Analytics Measurements ID"),
        required=False,
        help_text=_(
            "To locate your Measurement ID, navigate to Admin > Data Streams and ensure you're working with a Web Stream. Select the relevant stream, and the Measurement ID (in the format 'G-XXXXXXXXXX') will appear in the stream details at the top."
        ),
        max_length=12,
        min_length=12,
    )

    tracking_scripts_meta_pixel = forms.CharField(
        label=_("Meta Pixel Dataset ID"),
        required=False,
        help_text=_(
            "To locate your Dataset ID, go to Facebook Events Manager > Data Sources, select the relevant data source, click Settings, and find the Dataset ID. It will appear on this page in a format like 1253239248456634."
        ),
        max_length=20,
        min_length=10,
    )


class SettingsView(EventSettingsViewMixin, EventSettingsFormView):
    model = Event
    form_class = TrackingScriptsSettingsForm
    template_name = "pretix_tracking_scripts/settings.html"
    permission = "can_change_event_settings"

    def get_success_url(self):
        return reverse(
            "plugins:pretix_tracking_scripts:settings",
            kwargs={
                "organizer": self.request.event.organizer.slug,
                "event": self.request.event.slug,
            },
        )
