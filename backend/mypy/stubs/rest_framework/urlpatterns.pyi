from collections.abc import (
    Sequence,
)
from typing import (
    Optional,
)

from django.urls import (
    URLPattern,
)

def format_suffix_patterns(
    urlpatterns: Sequence[URLPattern],
    suffix_required: bool = False,
    allowed: Optional[Sequence[str]] = None,
) -> list[URLPattern]: ...
