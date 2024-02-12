from collections.abc import Mapping, Sequence
from typing import Any, Type

from django.db.models import Model

from rest_framework.request import Request
from rest_framework.views import APIView

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")

class BasePermissionMetaclass(type): ...

class BasePermission(metaclass=BasePermissionMetaclass):
    def has_permission(self, request: Request, view: APIView) -> bool: ...
    def has_object_permission(
        self, request: Request, view: APIView, obj: Any
    ) -> bool: ...

class AllowAny(BasePermission): ...
class IsAuthenticated(BasePermission): ...
class IsAdminUser(BasePermission): ...
class IsAuthenticatedOrReadOnly(BasePermission): ...

class DjangoModelPermissions(BasePermission):
    perms_map: Mapping[str, Sequence[str]]
    authenticated_users_only: bool
    def get_required_permissions(
        self, method: str, model_cls: Type[Model]
    ) -> Sequence[str]: ...
    def has_permission(self, request: Request, view: APIView) -> bool: ...

class DjangoModelPermissionsOrAnonReadOnly(DjangoModelPermissions): ...

class DjangoObjectPermissions(DjangoModelPermissions):
    def get_required_object_permissions(
        self, method: str, model_cls: Type[Model]
    ) -> Sequence[str]: ...
    def has_object_permission(
        self, request: Request, view: APIView, obj: Any
    ) -> bool: ...
