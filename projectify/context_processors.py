# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2021, 2023 JWP Consulting GK
"""Projectify context processors."""

from dataclasses import asdict
from typing import Mapping

from django.http import HttpRequest
from django.urls.resolvers import ResolverMatch

from projectify.lib.settings import get_settings
from projectify.settings.types import FeatureFlags


def show_go_to_dashboard(request: HttpRequest) -> Mapping[str, bool]:
    """Tell header nav that it can show "Go to dashboard"."""
    match request.resolver_match:
        case None:
            return {}
        case ResolverMatch(app_names=[]):
            return {}
        case ResolverMatch(app_names=["dashboard", *_]):
            result = False
        case ResolverMatch(app_names=[*_]):
            result = True
    return {"show_go_to_dashboard": result}


def feature_flags(request: HttpRequest) -> Mapping[str, Mapping[str, bool]]:
    """Pass feature flags to frontend."""
    del request
    settings = get_settings()
    # defensive programming so that this function doesn't return some other
    # important or secret stuff from the settings
    match settings.FEATURE_FLAGS:
        case FeatureFlags() as flags:
            return {"feature_flags": asdict(flags)}
