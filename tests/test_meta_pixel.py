#
# Copyright (C) 2025 Kian Cross
#

import re

import pytest

from .utils import TestBase


@pytest.mark.django_db
class TestMetaPixel(TestBase):
    def test_disabled(self, client, organizer, event):
        response = client.get("/%s/%s/" % (organizer.slug, event.slug), follow=True)

        assert b"https://connect.facebook.net/en_US/fbevents.js" not in response.content
        assert "https://connect.facebook.net" not in response["Content-Security-Policy"]

    def test_enabled_content(self, client, organizer, event):
        event.settings.tracking_scripts_meta_pixel = "9088776652899827"

        response = client.get("/%s/%s/" % (organizer.slug, event.slug), follow=True)

        assert response.status_code == 200
        assert b"https://connect.facebook.net/en_US/fbevents.js" in response.content
        assert b"9088776652899827" in response.content

    def test_enabled_headers(self, client, organizer, event):
        event.settings.tracking_scripts_meta_pixel = "9088776652899827"

        response = client.get("/%s/%s/" % (organizer.slug, event.slug), follow=True)

        assert "https://connect.facebook.net" in response["Content-Security-Policy"]

    def test_nonce(self, client, organizer, event):
        event.settings.tracking_scripts_meta_pixel = "9088776652899827"

        response = client.get("/%s/%s/" % (organizer.slug, event.slug), follow=True)

        nonce_match = re.search("nonce-([^ ']+)", response["Content-Security-Policy"])

        assert nonce_match
        assert nonce_match.group(1) in response.content.decode()
