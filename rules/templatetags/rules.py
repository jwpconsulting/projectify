# SPDX-FileCopyrightText: 2014 Akis Kesoglou
#
# SPDX-License-Identifier: MIT

from typing import TYPE_CHECKING, Any

from django import template

from ..rulesets import default_rules

if TYPE_CHECKING:
    from projectify.user.models.user import User

register = template.Library()


@register.simple_tag
def test_rule(name: str, obj: Any = None, target: Any = None) -> bool:
    return default_rules.test_rule(name, obj, target)


@register.simple_tag
def has_perm(perm: str, user: "User", obj: Any = None) -> bool:
    if not hasattr(user, "has_perm"):  # pragma: no cover
        return False  # swapped user model that doesn't support permissions
    else:
        return user.has_perm(perm, obj)
