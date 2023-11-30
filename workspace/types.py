"""Shared type definitions in workspace app."""
from typing import (
    Mapping,
    Optional,
    Sequence,
    TypedDict,
    Union,
)


class ConsumerEvent(TypedDict):
    """Contains event data about what to send to client."""

    type: str
    uuid: str


class Message(TypedDict):
    """Contains message to send to client."""

    type: str
    uuid: str
    # TODO Sequence required here?
    data: Optional[Union[Mapping[str, object], Sequence[object]]]
