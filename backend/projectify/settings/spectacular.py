# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2024 JWP Consulting GK
"""DRF-Spectacular settings."""


class SpectacularSettings:
    """Settings mixin used for drf-spectacular."""

    # drf-spectacular
    # from
    # https://drf-spectacular.readthedocs.io/en/latest/readme.html#installation
    SPECTACULAR_SETTINGS = {
        "TITLE": "Projectify backend API",
        "DESCRIPTION": "API for the Projectify project management software",
        "VERSION": "1.0.0",
        "SERVE_INCLUDE_SCHEMA": False,
        "SWAGGER_UI_DIST": "SIDECAR",  # shorthand to use the sidecar instead
        "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
        "REDOC_DIST": "SIDECAR",
        "PREPROCESSING_HOOKS": (
            "projectify.lib.error_schema.preprocess_derive_error_schemas",
        ),
    }

    SERVE_SPECTACULAR = True
