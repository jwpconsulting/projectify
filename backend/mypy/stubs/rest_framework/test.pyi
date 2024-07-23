from typing import (
    Any,
    Optional,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.test.client import Client as DjangoClient

import requests
from rest_framework.request import Request
from rest_framework.response import (
    Response,
)

# TODO would be cool if we could have data be the same SerializerData thing
# from serializers.pyi

# We ignore that APIRequestFactory inherits from DjangoRequestFactory,
# otherwise we'd get into Liskov trouble
class APIRequestFactory:
    def get(self, *args: Any, **kwargs: Any) -> Request: ...
    def post(self, *args: Any, **kwargs: Any) -> Request: ...
    def put(self, *args: Any, **kwargs: Any) -> Request: ...
    def patch(self, *args: Any, **kwargs: Any) -> Request: ...
    def options(self, *args: Any, **kwargs: Any) -> Request: ...
    def delete(self, *args: Any, **kwargs: Any) -> Request: ...

class APIClient(APIRequestFactory, DjangoClient):
    def force_authenticate(
        self,
        user: Optional[AbstractBaseUser] = None,
        token: Optional[str] = None,
    ) -> None: ...
    # This is the exact same signature as in rest_framework/test.py
    # But our django type stubs are in disagreement here!
    def get(  # type: ignore[override]
        self,
        path: str,
        data: Optional[Any] = None,
        follow: bool = False,
        **extra: object,
    ) -> Response: ...
    def post(  # type: ignore[override]
        self,
        path: str,
        data: Optional[Any] = None,
        format: Optional[str] = None,
        content_type: Optional[str] = None,
        **extra: object,
    ) -> Response: ...
    def patch(  # type: ignore[override]
        self,
        path: str,
        data: Optional[Any] = None,
        format: Optional[str] = None,
        content_type: Optional[str] = None,
        **extra: object,
    ) -> Response: ...
    def put(  # type: ignore[override]
        self,
        path: str,
        data: Optional[Any] = None,
        format: Optional[str] = None,
        content_type: Optional[str] = None,
        **extra: object,
    ) -> Response: ...
    def options(  # type: ignore[override]
        self,
        path: str,
        data: Optional[Any] = None,
        format: Optional[str] = None,
        content_type: Optional[str] = None,
        **extra: object,
    ) -> Response: ...
    def delete(  # type: ignore[override]
        self,
        path: str,
        data: Optional[Any] = None,
        format: Optional[str] = None,
        content_type: Optional[str] = None,
        follow: bool = False,
        **extra: object,
    ) -> Response: ...

class RequestsClient(requests.Session): ...
