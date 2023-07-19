from django.views import (
    View,
)

from . import (
    request,
)

class APIView(View):
    request: request.Request
