"""Shared type definitions in workspace app."""
from collections.abc import (
    Mapping,
    Sequence,
)
from typing import (
    TypedDict,
    Union,
)


class Message(TypedDict):
    """Contains message to send to client."""

    type: str
    uuid: str
    data: Union[Mapping[str, object], Sequence[object]]
