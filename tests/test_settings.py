#
# Copyright (C) 2025 Kian Cross
#

import pytest

from .utils import TestBase


@pytest.mark.django_db
class TestSettings(TestBase):
    def test_load_then_submit_then_load(
        self, client, organizer, event, admin_user, team
    ):
        client.login(email="foo@example.com", password="bar")

        response = client.get(
            "/control/event/%s/%s/settings/tracking-scripts/"
            % (organizer.slug, event.slug)
        )

        assert response.status_code == 200
        assert b"Tracking Scripts" in response.content

        response = client.post(
            "/control/event/%s/%s/settings/tracking-scripts/"
            % (organizer.slug, event.slug),
            {
                "tracking_scripts_google_analytics": "123456789101",
                "tracking_scripts_meta_pixel": "23982392328293823967",
            },
            follow=True,
        )

        assert response.status_code == 200
        assert b"Your changes have been saved." in response.content
        assert event.settings.tracking_scripts_google_analytics == "123456789101"
        assert event.settings.tracking_scripts_meta_pixel == "23982392328293823967"

        response = client.get(
            "/control/event/%s/%s/settings/tracking-scripts/"
            % (organizer.slug, event.slug)
        )

        assert response.status_code == 200
        assert b"Tracking Scripts" in response.content

    def test_plugins_page(self, client, organizer, event, admin_user, team):
        client.login(email="foo@example.com", password="bar")

        response = client.get(
            "/control/event/%s/%s/settings/plugins" % (organizer.slug, event.slug)
        )

        assert response.status_code == 200
        assert b"Pretix Tracking Scripts" in response.content
