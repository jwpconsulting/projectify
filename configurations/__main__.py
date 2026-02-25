# SPDX-FileCopyrightText: 2012-2023, Jannis Leidel and other contributors.
# SPDX-FileCopyrightText: 2025, UhuruTechnology
#
# SPDX-License-Identifier: BSD-3-Clause
# type: ignore

"""
invokes django-cadmin when the dj_configurator module is run as a script.

Example: python -m dj_configurator check
"""

from .management import execute_from_command_line

if __name__ == "__main__":
    execute_from_command_line()
