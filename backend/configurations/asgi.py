# SPDX-FileCopyrightText: 2012-2023, Jannis Leidel and other contributors.
# SPDX-FileCopyrightText: 2025, UhuruTechnology
#
# SPDX-License-Identifier: BSD-3-Clause
# type: ignore

from . import importer

importer.install()

from django.core.asgi import get_asgi_application  # noqa: E402

# this is just for the crazy ones
application = get_asgi_application()
