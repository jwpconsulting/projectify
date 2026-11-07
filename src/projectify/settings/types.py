# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2024,2026 JWP Consulting GK
"""Types used for settings."""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import (
    Any,
    Literal,
    Mapping,
    NotRequired,
    Optional,
    TypedDict,
    Union,
)


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

SocialAccountApp = TypedDict(
    "SocialAccountApp",
    {
        # Optional isn't the cleanest
        "client_id": Optional[str],
        "secret": Optional[str],
        # For openid_connect
        "provider_id": NotRequired[str],
        # For apple
        "key": NotRequired[str],
        "settings": NotRequired[dict[str, str]],
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


DjangoEmailBackendConfigOptions = TypedDict(
    "DjangoEmailBackendConfigOptions",
    {
        "host": str,
        "port": NotRequired[int],
        "use_tls": NotRequired[bool],
        "use_ssl": NotRequired[bool],
        "username": NotRequired[str],
        "password": NotRequired[str],
        "ssl_certfile": NotRequired[str],
        "ssl_keyfile": NotRequired[str],
        "timeout": NotRequired[int],
        "fail_silently": NotRequired[bool],
    },
)
DjangoEmailBackendConfig = TypedDict(
    "DjangoEmailBackendConfig",
    {
        "BACKEND": Literal["django.core.mail.backends.smtp.EmailBackend"],
        "OPTIONS": DjangoEmailBackendConfigOptions,
    },
)
DjangoEmailConsoleBackendConfig = TypedDict(
    "DjangoEmailConsoleBackendConfig",
    {"BACKEND": Literal["django.core.mail.backends.console.EmailBackend"]},
)
MailerConfig = Union[DjangoEmailBackendConfig, DjangoEmailConsoleBackendConfig]
