from typing import (
    Any,
    Optional,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.test.client import Client as DjangoClient
from django.test.client import RequestFactory as DjangoRequestFactory

from rest_framework.response import (
    Response,
)

class APIRequestFactory(DjangoRequestFactory): ...

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
        **extra: object
    ) -> Response: ...
    def post(  # type: ignore[override]
        self,
        path: str,
        data: Optional[Any],
        format: Optional[str] = None,
        content_type: Optional[str] = None,
        **extra: object
    ) -> Response: ...
    def put(  # type: ignore[override]
        self,
        path: str,
        data: Optional[Any],
        format: Optional[str] = None,
        content_type: Optional[str] = None,
        **extra: object
    ) -> Response: ...
