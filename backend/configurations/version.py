# SPDX-FileCopyrightText: 2012-2023, Jannis Leidel and other contributors.
# SPDX-FileCopyrightText: 2025, UhuruTechnology
#
# SPDX-License-Identifier: BSD-3-Clause
# type: ignore

import typing
from importlib.metadata import PackageNotFoundError, version

try:
    __version__: typing.Optional[str] = version("django-configurator")
except PackageNotFoundError:
    # package is not installed
    __version__ = None
