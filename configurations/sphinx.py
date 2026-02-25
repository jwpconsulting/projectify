# SPDX-FileCopyrightText: 2012-2023, Jannis Leidel and other contributors.
# SPDX-FileCopyrightText: 2025, UhuruTechnology
#
# SPDX-License-Identifier: BSD-3-Clause
# type: ignore

from . import _setup, __version__


def setup(app=None):
    """
    The callback for Sphinx that acts as a Sphinx extension to use doc strings in Sphinx documentation.

    Add ``'dj_configurator'`` to the ``extensions`` config variable
    in your docs' ``conf.py``.
    """
    _setup()
    return {"version": __version__, "parallel_read_safe": True}
