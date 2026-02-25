# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Types used for settings."""

from collections.abc import Sequence
from typing import Any, Mapping, TypedDict


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
