from typing import (
    Optional,
)

from django.template.response import (
    SimpleTemplateResponse,
)

class Response(SimpleTemplateResponse):
    def __init__(
        self,
        data: Optional[object] = None,
        status: Optional[int] = None,
        template_name: Optional[str] = None,
        headers: Optional[object] = None,
        exception: bool = False,
        content_type: Optional[str] = None,
    ) -> None: ...
