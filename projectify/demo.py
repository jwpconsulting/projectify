# SPDX-License-Identifier: MIT
#
# SPDX-FileCopyrightText: 2009-2026 (c) Benoît Chesneau <benoitc@gunicorn.org>
# SPDX-FileCopyrightText: 2009-2015 (c) Paul J. Davis <paul.joseph.davis@gmail.com>


"""Projectify demo command."""

import os
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any, Callable, Optional, Union

# https://gunicorn.org/custom/
from gunicorn.app.base import BaseApplication  # type: ignore


class StandaloneApplication(BaseApplication):  # type: ignore
    """Standalone WSGI app based on gunicorn example."""

    def __init__(
        self,
        app: Callable[[Any, Any], Any],
        options: Optional[Mapping[str, Union[str, int, None]]] = None,
    ):
        """Initialize app."""
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self) -> None:
        """Load configuration."""
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self) -> Any:
        """Return application."""
        return self.application


def _main(tmpdir: str) -> None:
    """Take tmpdir, run Projectify demo."""
    db_path = Path(tmpdir) / "demo.db"
    static_path = Path(tmpdir) / "static"

    print(f"Creating temporary database at: {db_path}")
    print(f"Creating temporary static files directory at: {static_path}")

    env = os.environ
    env["DATABASE_URL"] = f"sqlite:///{db_path}"
    env["STATIC_ROOT"] = str(static_path)
    env["DJANGO_SETTINGS_MODULE"] = "projectify.settings.demo"
    env["DJANGO_CONFIGURATION"] = "Demo"

    from configurations.management import (  # type: ignore
        execute_from_command_line,
    )

    execute_from_command_line([".", "seeddb"])
    execute_from_command_line([".", "collectstatic", "--noinput"])

    print("Starting Projectify demo server")
    print("Address: http://localhost:8100")
    print("Admin login:")
    print("Username: admin@localhost")
    print("Password: password")
    print("=" * 60)

    from projectify.wsgi import application

    StandaloneApplication(
        application, {"bind": "127.0.0.1:8100", "workers": 1}
    ).run()


def main() -> None:
    """Run Projectify demo with temporary database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        _main(tmpdir)


if __name__ == "__main__":
    main()
