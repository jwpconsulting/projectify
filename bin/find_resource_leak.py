#!/usr/bin/env python3
"""
Find out why we forget to close a Python file.

The resource warning in question is only met when pytest on possibly any test
with xtest enabled.

Exception ignored in: <_io.FileIO name='/home/$HOME/projects/projectify/projectify-backend/projectify/settings/test.py' mode='rb' closefd=True>
Traceback (most recent call last):
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
ResourceWarning: unclosed file <_io.TextIOWrapper name='/home/$HOME/projects/projectify/projectify-backend/projectify/settings/test.py' mode='r' encoding='utf-8'>

The idea is to use an audit hook to see when this file is opened.

Update: The offending line is most likely this:

https://github.com/jazzband/django-configurations/blob/dd5d6974cb9a646cf898ad36ba001b07b2199da1/configurations/importer.py#L133

find_module

Our stack trace was:
open(/home/$USER/projects/projectify/projectify-backend/projectify/settings/test.py, ['r', 524288])
projects/projectify/projectify-backend/bin/find_resource_leak.py:audit_open:127
projects/projectify/projectify-backend/bin/find_resource_leak.py:audit_hook:133
/usr/lib/python3.11/imp.py:find_module:303
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/configurations/importer.py:find_module:133
<frozen importlib._bootstrap>:_find_spec_legacy:1050
<frozen importlib._bootstrap>:_find_spec:1076
<frozen importlib._bootstrap>:_find_and_load_unlocked:1140
<frozen importlib._bootstrap>:_find_and_load:1178
<frozen importlib._bootstrap>:_gcd_import:1206
/usr/lib/python3.11/importlib/__init__.py:import_module:126
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/django/conf/__init__.py:__init__:217
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/django/conf/__init__.py:_setup:89
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/django/conf/__init__.py:__getattr__:102
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/pytest_django/plugin.py:pytest_load_initial_conftests:351
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/pluggy/_callers.py:_multicall:77
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/pluggy/_manager.py:_hookexec:115
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/pluggy/_hooks.py:__call__:493
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/_pytest/config/__init__.py:_preparse:1250
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/_pytest/config/__init__.py:parse:1348
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/_pytest/config/__init__.py:pytest_cmdline_parse:1060
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/pluggy/_callers.py:_multicall:77
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/pluggy/_manager.py:_hookexec:115
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/pluggy/_hooks.py:__call__:493
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/_pytest/config/__init__.py:_prepareconfig:329
.cache/pypoetry/virtualenvs/projectify_backend-6QKmYSTv-py3.11/lib/python3.11/site-packages/_pytest/config/__init__.py:main:148
projects/projectify/projectify-backend/bin/find_resource_leak.py:<module>:142
Exception ignored in: <_io.FileIO name='/home/$USER/projects/projectify/projectify-backend/projectify/settings/test.py' mode='rb' closefd=True>
Traceback (most recent call last):
  File "<frozen importlib._bootstrap>", line 1178, in _find_and_load
ResourceWarning: unclosed file <_io.TextIOWrapper name='/home/$USER/projects/projectify/projectify-backend/projectify/settings/test.py' mode='r' encoding='utf-8'>

This tells me that django-configurations gets a file handle on a Django
settings file, but doesn't close it - presumably. I was not able to find any
other relevant open() calls.

OTOH, it could be that due to forking we have another open() call somewhere
that we don't catch using an audit hook.
"""
import inspect
import sys
from collections.abc import (
    Sequence,
)
from pathlib import (
    Path,
)

import pytest


def print_caller() -> None:
    """Print caller information, up to 100 frames."""
    caller = inspect.currentframe()
    if caller is None:
        raise Exception("Expected caller")
    caller_info: list[tuple[Path, str, int]] = []
    for _ in range(100):
        caller = caller.f_back
        if caller is None:
            break
        caller_info.append(
            (
                Path(caller.f_code.co_filename),
                caller.f_code.co_name,
                caller.f_lineno,
            )
        )
    home = Path.home()
    for path, name, line in caller_info:
        if path.is_relative_to(home):
            path = path.relative_to(home)
        print(":".join((str(path), name, str(line))))


def audit_open(args: Sequence[object]) -> None:
    """Check for an open call for file projectify/settings/test.py."""
    file, *rest = args
    if isinstance(file, int):
        return
    elif not isinstance(file, str):
        return
    if "projectify/settings/test.py" not in file:
        return
    print(f"open({file}, {rest})")
    print_caller()


def audit_hook(event: str, args: Sequence[object]) -> None:
    """Check if event is open, if yes, call audit_open()."""
    if event == "open":
        audit_open(args)
    else:
        return


sys.addaudithook(audit_hook)


if __name__ == "__main__":
    retcode = pytest.main(
        [
            "-n",
            "1",
            "workspace/test/views/test_workspace.py::TestInviteUserToWorkspace::test_new_user",
        ]
    )
    sys.exit(retcode)
