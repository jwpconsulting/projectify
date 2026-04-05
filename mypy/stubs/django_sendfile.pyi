# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""django_sendfile type stub."""

from typing import Optional

from django.http import HttpRequest, HttpResponse

def sendfile(
    request: HttpRequest,
    filename: str,
    attachment: bool = False,
    attachment_filename: Optional[str] = None,
    mimetype: Optional[str] = None,
    encoding: Optional[str] = None,
    content_length: Optional[int] = None,
) -> HttpResponse: ...
