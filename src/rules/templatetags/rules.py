# SPDX-FileCopyrightText: 2014 Akis Kesoglou
#
# SPDX-License-Identifier: MIT

from typing import TYPE_CHECKING, Any

from django import template

from projectify.lib.auth import PermissionsCache, validate_perm

from ..rulesets import default_rules

if TYPE_CHECKING:
    from projectify.user.models import User

register = template.Library()


@register.simple_tag
def test_rule(name: str, obj: Any = None, target: Any = None) -> bool:
    return default_rules.test_rule(name, obj, target)


@register.simple_tag(takes_context=True)
def has_perm(context: dict[str, Any], perm: str, user: "User", obj: Any = None) -> bool:
    if not hasattr(user, "has_perm"):  # pragma: no cover
        return False  # swapped user model that doesn't support permissions

    cache: PermissionsCache
    if "_perm_cache" not in context:
        cache = {}
        context["_perm_cache"] = cache
    else:
        cache = context["_perm_cache"]
    return validate_perm(perm, user, obj, raise_exception=False, cache=cache)
