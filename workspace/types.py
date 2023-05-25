"""Shared type definitions in workspace app."""
from collections.abc import (
    Mapping,
)
from typing import (
    TypedDict,
)


class Message(TypedDict):
    """Contains message to send to client."""

    type: str
    uuid: str
    data: Mapping[str, object]
