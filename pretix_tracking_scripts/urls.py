#
# Copyright (C) 2024 Kian Cross
#

from django.urls import re_path

from .views import SettingsView

urlpatterns = [
    re_path(
        r"^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/settings/tracking-scripts/$",
        SettingsView.as_view(),
        name="settings",
    ),
]
