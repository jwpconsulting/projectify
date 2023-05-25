from typing import (
    Any,
    Callable,
    Generic,
    Optional,
    ParamSpec,
)

P = ParamSpec("P")

class Predicate(Generic[P]):

    __call__: Callable[P, bool]

    def __and__(self, other: Predicate[P]) -> Predicate[P]: ...

PredicateFn = Callable[P, bool]

def predicate(
    fn: Optional[PredicateFn[P]] = None, name: Optional[str] = None
) -> Predicate[P]: ...
def add_perm(name: str, pred: Predicate[Any]) -> None: ...
