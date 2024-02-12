from collections.abc import (
    Mapping,
)
from typing import (
    Any,
    Generic,
    TypeVar,
)

from django.db import (
    models,
)

from .request import (
    Request,
)
from .response import (
    Response,
)

M = TypeVar("M", bound=models.Model)
# TODO I want to be able to say bound=ModelSerializer[M] here
S = TypeVar("S")

class CreateModelMixin(Generic[M, S]):
    def create(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response: ...
    def perform_create(self, serializer: S) -> None: ...
    def get_success_headers(
        self, data: Mapping[str, Any]
    ) -> Mapping[str, Any]: ...

class ListModelMixin(Generic[M]):
    def list(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response: ...

class RetrieveModelMixin(Generic[M]):
    def retrieve(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response: ...

class UpdateModelMixin(Generic[M, S]):
    def update(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response: ...
    def perform_update(self, serializer: S) -> None: ...
    def partial_update(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response: ...

class DestroyModelMixin(Generic[M]):
    def perform_destroy(self, instance: M) -> None: ...
