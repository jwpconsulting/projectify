# SPDX-FileCopyrightText: 2024 JWP Consulting GK
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Any, Optional

from django.template.response import SimpleTemplateResponse

class Response(SimpleTemplateResponse):
    data: Any

    def __init__(
        self,
        data: Optional[object] = None,
        status: Optional[int] = None,
        template_name: Optional[str] = None,
        headers: Optional[object] = None,
        exception: bool = False,
        content_type: Optional[str] = None,
    ) -> None: ...
