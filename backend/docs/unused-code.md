# Unused code

Unused code is unavoidable in any project during its growth.

There are a few heuristics on determining whether we are using something or
not. One tool that seems to do part of the job is vulture. It's added to the
poetry dependencies and can be run (with the existing whitelist) using

```
poetry run vulture .
```

It gives a lot of false positives. Unfortunately, due to the declarative
nature of the frameworks that we use here (Django and DRF), it can't tell
with certainty whether a certain declaration is ever used or not. On the other
hand, if we use coverage metrics, classes will be always evaluated when
booting up the application, but that doesn't mean that a class is used or not.
Coverage is mostly suitable for detecting whether method code is run or not.

So we can use vulture as an occasional check for things that might have
slipped through the cracks, but not more. That doesn't mean it's not useful,
it's just not helpful to make it part of the CI process at this point in time.
