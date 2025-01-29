#
# Copyright (C) 2025 Kian Cross
#

import pytest
from django.utils import timezone
from django_scopes import scopes_disabled
from pretix.base.models import Organizer, Team, User


@pytest.mark.django_db
class TestBase:
    @pytest.fixture()
    def organizer(self):
        return Organizer.objects.create(name="Test Organizer", slug="TO")

    @pytest.fixture()
    @scopes_disabled()
    def event(self, organizer):
        return organizer.events.create(
            name="Test Event",
            slug="TE",
            date_from=timezone.now() + timezone.timedelta(days=1),
            plugins="pretix.plugins.banktransfer,pretix_tracking_scripts",
            live=True,
        )

    @pytest.fixture()
    @scopes_disabled()
    def admin_user(self):
        return User.objects.create_user("foo@example.com", "bar")

    @pytest.fixture()
    @scopes_disabled()
    def team(self, organizer, event, admin_user):
        team = Team.objects.create(
            organizer=organizer,
            can_create_events=True,
            can_change_event_settings=True,
            can_change_items=True,
            can_change_organizer_settings=True,
        )
        team.members.add(admin_user)
        team.limit_events.add(event)
        return team
