from abc import (
    ABCMeta,
    abstractmethod,
)
from typing import (
    Optional,
)

class BaseChannelLayer(metaclass=ABCMeta):
    async def group_send(
        self, group: str, message: dict[str, object]
    ) -> None: ...
    @abstractmethod
    def group_add(self, group: str, channel: str) -> None: ...
    @abstractmethod
    def group_discard(self, group: str, channel: str) -> None: ...

def get_channel_layer() -> Optional[BaseChannelLayer]: ...
