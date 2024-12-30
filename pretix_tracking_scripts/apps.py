#
# Copyright (C) 2024 Kian Cross
#

import importlib.metadata

from django.utils.safestring import mark_safe
from django.utils.translation import gettext, gettext_lazy
from pretix.base.plugins import PluginConfig


class PluginApp(PluginConfig):
    default = True
    name = "pretix_tracking_scripts"
    verbose_name = "Pretix Tracking Scripts"

    class PretixPluginMeta:
        name = gettext_lazy("Pretix Tracking Scripts")
        author = "Kian Cross"
        visible = True
        version = importlib.metadata.version("pretix_tracking_scripts")
        category = "INTEGRATION"
        compatibility = "pretix>=2023.6.2"

        @property
        def description(self):
            return mark_safe(
                gettext("Adds scripts for analytics and conversion tracking to pretix.")
            )

    def ready(self):
        from . import signals
