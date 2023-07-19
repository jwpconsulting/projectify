from typing import (
    Any,
    Mapping,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
)
from django.http import (
    HttpRequest,
)

# XXX
# The inheritance is not entirely accurate.
# In drf, Request wraps HttpRequest, instead of subclassing it. Unfortunately,
# since drf APIViews subclass django's view, the request attribute has to be
# subclassed from it
# See this error:
# mypy/stubs/rest_framework/views.pyi:10: error: Incompatible types in assignment (expression has type "Request", base class "View" defined the type as "HttpRequest")  [assignment]
# This isn't possible for us so we tell mypy that Request inherits from
# HttpRequest even though that is not true
class Request(HttpRequest):
    # XXX
    # We are conveniently ignoring for now that the user can be Anonymous as well
    user: AbstractBaseUser
    data: Mapping[str, Any]
