# SPDX-FileCopyrightText: 2024 JWP Consulting GK
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# Taken from
# https://raw.githubusercontent.com/encode/django-rest-framework/3.14.0/rest_framework/exceptions.py
from collections.abc import Mapping, Sequence
from typing import Optional, Union

ErrorMessage = Union[str, Sequence[ErrorMessage], Mapping[str, ErrorMessage]]
Code = str

class ErrorDetail(str):
    code: Union[str, int, None]

class APIException(Exception):
    status_code: int
    default_detail: str
    default_code: str
    detail: ErrorMessage

    def __init__(
        self,
        detail: Optional[ErrorMessage] = None,
        code: Optional[Code] = None,
    ) -> None: ...
    def get_codes(self) -> ErrorMessage: ...
    def get_full_details(self) -> ErrorMessage: ...

class ValidationError(APIException): ...
