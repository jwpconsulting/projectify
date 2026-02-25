# SPDX-FileCopyrightText: 2024 JWP Consulting GK
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from typing import Any, Optional

from rest_framework.fields import Field

class RelatedField(Field):
    def __init__(self, **kwargs: Any) -> None: ...

class SlugRelatedField(RelatedField):
    def __init__(
        self, slug_field: Optional[str] = None, **kwargs: Any
    ) -> None: ...
