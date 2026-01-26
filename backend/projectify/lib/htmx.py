# SPDX-FileCopyrightText: 2020 Adam Johnson
# SPDX-License-Identifier: MIT
# HTMX code vendored in. See docs
# https://django-htmx.readthedocs.io/en/latest/
# https://github.com/adamchainz/django-htmx/blob/e18a0c8cc3f97c2ced7b6f939fb2b487563712f9/src/django_htmx/middleware.py
# Full license
# Either in this repository's LICENSES directory or
# at
# https://github.com/adamchainz/django-htmx/blob/main/LICENSE
"""HTMX Middleware from django-htmx library."""

# ruff: noqa: D101, D102, D105, D107
import json
from collections.abc import Awaitable
from inspect import iscoroutinefunction, markcoroutinefunction
from typing import Any, Callable
from urllib.parse import unquote, urlsplit, urlunsplit

from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponseBase, HttpResponseRedirectBase
from django.utils.functional import cached_property


class HtmxMiddleware:
    sync_capable = True
    async_capable = True

    def __init__(
        self,
        get_response: (
            Callable[[HttpRequest], HttpResponseBase]
            | Callable[[HttpRequest], Awaitable[HttpResponseBase]]
        ),
    ) -> None:
        self.get_response = get_response
        self.async_mode = iscoroutinefunction(self.get_response)

        if self.async_mode:
            # Mark the class as async-capable, but do the actual switch
            # inside __call__ to avoid swapping out dunder methods
            markcoroutinefunction(self)

    def __call__(
        self, request: HttpRequest
    ) -> HttpResponseBase | Awaitable[HttpResponseBase]:
        if self.async_mode:
            return self.__acall__(request)
        request.htmx = HtmxDetails(request)  # type: ignore [attr-defined]
        return self.get_response(request)

    async def __acall__(self, request: HttpRequest) -> HttpResponseBase:
        request.htmx = HtmxDetails(request)  # type: ignore [attr-defined]
        return await self.get_response(request)  # type: ignore [no-any-return, misc]


class HtmxDetails:
    def __init__(self, request: HttpRequest) -> None:
        self.request = request

    def _get_header_value(self, name: str) -> str | None:
        value = self.request.headers.get(name) or None
        if value:
            if self.request.headers.get(f"{name}-URI-AutoEncoded") == "true":
                value = unquote(value)
        return value

    def __bool__(self) -> bool:
        return self._get_header_value("HX-Request") == "true"

    @cached_property
    def boosted(self) -> bool:
        return self._get_header_value("HX-Boosted") == "true"

    @cached_property
    def current_url(self) -> str | None:
        return self._get_header_value("HX-Current-URL")

    @cached_property
    def current_url_abs_path(self) -> str | None:
        url = self.current_url
        if url is not None:
            split = urlsplit(url)
            if (
                split.scheme == self.request.scheme
                and split.netloc == self.request.get_host()
            ):
                url = urlunsplit(split._replace(scheme="", netloc=""))
            else:
                url = None
        return url

    @cached_property
    def history_restore_request(self) -> bool:
        return self._get_header_value("HX-History-Restore-Request") == "true"

    @cached_property
    def prompt(self) -> str | None:
        return self._get_header_value("HX-Prompt")

    @cached_property
    def target(self) -> str | None:
        return self._get_header_value("HX-Target")

    @cached_property
    def trigger(self) -> str | None:
        return self._get_header_value("HX-Trigger")

    @cached_property
    def trigger_name(self) -> str | None:
        return self._get_header_value("HX-Trigger-Name")

    @cached_property
    def triggering_event(self) -> Any:
        value = self._get_header_value("Triggering-Event")
        if value is not None:
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                value = None
        return value


class HttpResponseClientRedirect(HttpResponseRedirectBase):
    status_code = 200

    def __init__(self, redirect_to: str, *args: Any, **kwargs: Any) -> None:
        if kwargs.get("preserve_request"):
            raise ValueError(
                "The 'preserve_request' argument is not supported for "
                "HttpResponseClientRedirect.",
            )
        super().__init__(redirect_to, *args, **kwargs)
        self["HX-Redirect"] = self["Location"]
        del self["Location"]

    @property
    def url(self) -> str:
        return self["HX-Redirect"]


class HttpResponseClientRefresh(HttpResponse):
    def __init__(self) -> None:
        super().__init__()
        self["HX-Refresh"] = "true"
