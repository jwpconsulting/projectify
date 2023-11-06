from typing import (
    Optional,
)

from ..consumer import (
    SyncConsumer,
)

class WebsocketConsumer(SyncConsumer):
    def connect(self) -> None: ...
    def accept(self, subprotocol: Optional[str] = None) -> None: ...
    def close(self, code: Optional[int] = None) -> None: ...

class JsonWebsocketConsumer(WebsocketConsumer):
    def send_json(
        self, content: object, close: Optional[bool] = False
    ) -> None: ...
