# SPDX-FileCopyrightText: 2014 Akis Kesoglou
#
# SPDX-License-Identifier: MIT

from django.apps import AppConfig


class RulesConfig(AppConfig):
    name = "rules"
    default = True


class AutodiscoverRulesConfig(RulesConfig):
    default = False

    def ready(self) -> None:
        from django.utils.module_loading import autodiscover_modules

        autodiscover_modules("rules")
