from typing import (
    Any,
    Generic,
    Mapping,
    Optional,
    Type,
    TypedDict,
    TypeVar,
)

from django.db import (
    models,
)

from . import (
    mixins,
    views,
)
from .request import (
    Request,
)
from .response import (
    Response,
)
from .serializers import (
    Serializer,
)

M = TypeVar("M", bound=models.Model)
# Ideally, this would be bound to a QuerySet of M
# So, Q = TypeVar("Q", models.QuerySet[M])
Q = TypeVar("Q")
# Serializer
S = TypeVar("S", bound=Serializer)

def get_object_or_404(
    queryset: models.QuerySet[M], *filter_args: object, **filter_kwargs: object
) -> M: ...

class SerializerContext(Generic[M, Q, S], TypedDict):

    request: Request
    format: str
    view: GenericAPIView[M, Q, S]

class GenericAPIView(Generic[M, Q, S], views.APIView):
    lookup_field: str = "pk"
    queryset: Q

    # TODO paginator: BasePagination
    def get_queryset(self) -> Q: ...
    def get_object(self) -> M: ...
    def get_serializer(
        self,
        instance: Optional[M] = None,
        data: Optional[Mapping[str, Any]] = None,
        partial: Optional[bool] = False,
    ) -> S: ...
    def get_serializer_class(self) -> Type[S]: ...
    def get_serializer_context(self) -> SerializerContext[M, Q, S]: ...
    def filter_queryset(self, queryset: Q) -> Q: ...
    # TODO def paginate_queryset(self, queryset: Q) -> Page
    # TODO def get_pagined_response(self, data: Any) -> Response

class CreateAPIView(
    Generic[M, Q, S], mixins.CreateModelMixin[M, S], GenericAPIView[M, Q, S]
):
    def post(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response: ...

class ListAPIView(
    Generic[M, Q, S], mixins.ListModelMixin[M], GenericAPIView[M, Q, S]
):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...

class RetrieveAPIView(
    Generic[M, Q, S], mixins.RetrieveModelMixin[M], GenericAPIView[M, Q, S]
):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...

class DestroyAPIView(
    Generic[M, Q, S], mixins.DestroyModelMixin[M], GenericAPIView[M, Q, S]
):
    def delete(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response: ...

class UpdateAPIView(
    Generic[M, Q, S], mixins.UpdateModelMixin[M, S], GenericAPIView[M, Q, S]
):
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def patch(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response: ...

class ListCreateAPIView(
    Generic[M, Q, S],
    mixins.ListModelMixin[M],
    mixins.CreateModelMixin[M, S],
    GenericAPIView[M, Q, S],
):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def post(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response: ...

class RetrieveUpdateAPIView(
    Generic[M, Q, S],
    mixins.RetrieveModelMixin[M],
    mixins.UpdateModelMixin[M, S],
    GenericAPIView[M, Q, S],
):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def patch(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response: ...

class RetrieveDestroyAPIView(
    Generic[M, Q, S],
    mixins.RetrieveModelMixin[M],
    mixins.DestroyModelMixin[M],
    GenericAPIView[M, Q, S],
):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def delete(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response: ...

class RetrieveUpdateDestroyAPIView(
    Generic[M, Q, S],
    mixins.RetrieveModelMixin[M],
    mixins.UpdateModelMixin[M, S],
    mixins.DestroyModelMixin[M],
    GenericAPIView[M, Q, S],
):
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response: ...
    def patch(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response: ...
    def delete(
        self, request: Request, *args: Any, **kwargs: Any
    ) -> Response: ...
