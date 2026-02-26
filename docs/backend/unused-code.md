<!--
SPDX-FileCopyrightText: 2024 JWP Consulting GK

SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Unused code

Unused code is unavoidable in any project during its growth.

There are a few heuristics on determining whether we are using something or
not. One tool that seems to do part of the job is [Vulture](https://github.com/jendrikseipp/vulture). It's part of the
Python project dependencies. Here's how to run it:

```
uv run vulture .
```

It gives a lot of false positives. Unfortunately, due to the declarative nature
of the frameworks that we use here (Django and DRF), it can't tell with
certainty whether a certain declaration is ever used or not. On the other hand,
if we use coverage metrics, classes will be always evaluated when booting up
the application, but that doesn't mean that a class is used or not. Coverage is
mostly suitable for detecting whether method code is run or not.

So we can use vulture as an occasional check for things that might have slipped
through the cracks, but not more. That doesn't mean it's not useful, it's just
not helpful to make it part of the CI process at this point in time.
