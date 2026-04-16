# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024,2026 JWP Consulting GK
"""Types used for settings."""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Mapping, NotRequired, Optional, TypedDict


class TemplateConfig(TypedDict):
    """Configure one templating module."""

    BACKEND: str
    APP_DIRS: bool
    OPTIONS: Mapping[str, Any]


TemplatesConfig = Sequence[TemplateConfig]


class StorageConfig(TypedDict):
    """Configuration for a storage."""

    BACKEND: str


StoragesConfig = Mapping[str, StorageConfig]

LoggingConfig = TypedDict(
    "LoggingConfig",
    {
        "version": int,
        "disable_existing_loggers": bool,
        "formatters": dict[str, Any],
        "handlers": dict[str, Any],
        "loggers": dict[str, Any],
    },
)

SocialAccountApp = TypedDict(
    "SocialAccountApp",
    {
        # Optional isn't the cleanest
        "client_id": Optional[str],
        "secret": Optional[str],
        # For openid_connect
        "provider_id": NotRequired[str],
    },
)

SocialAccountProvider = TypedDict(
    "SocialAccountProvider",
    {
        "EMAIL_AUTHENTICATION": NotRequired[bool],
        "SCOPE": NotRequired[list[str]],
        "APPS": list[SocialAccountApp],
    },
)


@dataclass
class StripeConfig:
    """Hold configuration needed to use Stripe."""

    # XXX it doesn't look like Projectify is using the publishable key
    # TODO consider removing the STRIPE_PUBLISHABLE_KEY
    STRIPE_PUBLISHABLE_KEY: str
    STRIPE_SECRET_KEY: str
    STRIPE_ENDPOINT_SECRET: str
    STRIPE_PRICE_OBJECT: str
