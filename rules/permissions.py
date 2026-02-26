# SPDX-FileCopyrightText: 2014 Akis Kesoglou
#
# SPDX-License-Identifier: MIT

from typing import TYPE_CHECKING, Any, ParamSpec

from .rulesets import RuleSet

if TYPE_CHECKING:
    from projectify.user.models import User  # noqa
    from . import Predicate

P = ParamSpec("P")

permissions = RuleSet[Any]()


def add_perm(name: str, pred: "Predicate[P]") -> None:
    permissions.add_rule(name, pred)


def set_perm(name: str, pred: "Predicate[P]") -> None:
    permissions.set_rule(name, pred)


def remove_perm(name: str) -> None:
    permissions.remove_rule(name)


def perm_exists(name: str) -> bool:
    return permissions.rule_exists(name)


def has_perm(name: str, *args: Any, **kwargs: Any) -> bool:
    return permissions.test_rule(name, *args, **kwargs)


class ObjectPermissionBackend(object):
    def authenticate(self, *args: Any, **kwargs: Any) -> None:
        return None

    def has_perm(
        self, user: "User", perm: str, *args: Any, **kwargs: Any
    ) -> bool:
        return has_perm(perm, user, *args, **kwargs)

    def has_module_perms(self, user: "User", app_label: str) -> bool:
        return has_perm(app_label, user)
