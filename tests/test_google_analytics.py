#
# Copyright (C) 2025 Kian Cross
#

import re

import pytest

from .utils import TestBase


@pytest.mark.django_db
class TestGoogleAnalytics(TestBase):
    def test_disabled(self, client, organizer, event):
        response = client.get("/%s/%s/" % (organizer.slug, event.slug), follow=True)

        assert b"https://www.googletagmanager.com/gtm.js" not in response.content
        assert "www.googletagmanager.com" not in response["Content-Security-Policy"]

    def test_enabled(self, client, organizer, event):
        event.settings.tracking_scripts_google_analytics = "123456789101"

        response = client.get("/%s/%s/" % (organizer.slug, event.slug), follow=True)

        assert response.status_code == 200
        assert b"https://www.googletagmanager.com/gtm.js" in response.content
        assert b"123456789101" in response.content

    def test_enabled_headers(self, client, organizer, event):
        event.settings.tracking_scripts_google_analytics = "123456789101"

        response = client.get("/%s/%s/" % (organizer.slug, event.slug), follow=True)

        assert "www.googletagmanager.com" in response["Content-Security-Policy"]

    def test_nonce(self, client, organizer, event):
        event.settings.tracking_scripts_google_analytics = "123456789101"

        response = client.get("/%s/%s/" % (organizer.slug, event.slug), follow=True)

        nonce_match = re.search("nonce-([^ ']+)", response["Content-Security-Policy"])

        assert nonce_match
        assert nonce_match.group(1) in response.content.decode()
