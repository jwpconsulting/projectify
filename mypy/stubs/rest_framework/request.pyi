from typing import (
    Any,
)

from django.http import (
    HttpRequest,
)

# Cheat and use our own user type
from projectify.user.models import User

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
    # It's not perfect, but we are just using our own User model here for now
    # Otherwise we have so many issues like AbstractUser providing has_perm
    # but not AbstractBaseUser, but our user inheriting from AbstractBaseUser
    user: User
    data: dict[str, Any]
