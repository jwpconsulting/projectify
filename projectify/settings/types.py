"""Types used for settings."""
from collections.abc import (
    Sequence,
)
from typing import (
    Any,
    Mapping,
    TypedDict,
)


ChannelLayer = Mapping[str, Any]
ChannelLayers = Mapping[str, ChannelLayer]


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
