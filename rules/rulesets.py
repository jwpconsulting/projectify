# SPDX-FileCopyrightText: 2014 Akis Kesoglou
#
# SPDX-License-Identifier: MIT

from typing import Any, ParamSpec, Union

from .predicates import Predicate, predicate

P = ParamSpec("P")


class RuleSet(dict[str, Predicate[P]]):
    def test_rule(self, name: str, *args: Any, **kwargs: Any) -> bool:
        return name in self and self[name].test(*args, **kwargs)

    def rule_exists(self, name: str) -> bool:
        return name in self

    def add_rule(self, name: str, pred: Union[Predicate[P], Any]) -> None:
        if name in self:
            raise KeyError("A rule with name `%s` already exists" % name)
        self[name] = pred

    def set_rule(self, name: str, pred: Union[Predicate[P], Any]) -> None:
        self[name] = pred

    def remove_rule(self, name: str) -> None:
        del self[name]

    def __setitem__(self, name: str, pred: Union[Predicate[P], Any]) -> None:
        fn = predicate(pred)
        super().__setitem__(name, fn)


# Shared rule set

default_rules = RuleSet[Any]()


def add_rule(name: str, pred: Union[Predicate[P], Any]) -> None:
    default_rules.add_rule(name, pred)


def set_rule(name: str, pred: Union[Predicate[P], Any]) -> None:
    default_rules.set_rule(name, pred)


def remove_rule(name: str) -> None:
    default_rules.remove_rule(name)


def rule_exists(name: str) -> bool:
    return default_rules.rule_exists(name)


def test_rule(name: str, *args: Any, **kwargs: Any) -> bool:
    return default_rules.test_rule(name, *args, **kwargs)
