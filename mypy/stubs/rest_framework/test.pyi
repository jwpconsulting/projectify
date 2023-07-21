from typing import (
    Optional,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.test.client import Client as DjangoClient
from django.test.client import RequestFactory as DjangoRequestFactory

class APIRequestFactory(DjangoRequestFactory): ...

class APIClient(APIRequestFactory, DjangoClient):
    def force_authenticate(
        self,
        user: Optional[AbstractBaseUser] = None,
        token: Optional[str] = None,
    ) -> None: ...
