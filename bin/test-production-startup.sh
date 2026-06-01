#!/usr/bin/env sh
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
#
# Test production startup with Hetzner settings class
set -e

export DJANGO_SETTINGS_MODULE="projectify.settings.hetzner"
export DJANGO_CONFIGURATION="Hetzner"

STATIC_ROOT=$(mktemp -d)
MEDIA_ROOT=$(mktemp -d)

CREDENTIALS_FILE=$(mktemp -d)/credentials.toml

export STATIC_ROOT MEDIA_ROOT CREDENTIALS_FILE

export PYTHON_DOTENV_DISABLED=1
echo "Note: Disabled load_dotenv() behavior in manage.py by setting"
echo "PYTHON_DOTENV_DISABLED=1"

cat > "$CREDENTIALS_FILE" << 'EOF'
SECRET_KEY = "test-secret-key-for-startup-check"

ADMIN_NAME = "Test Admin"
ADMIN_EMAIL = "admin@example.com"

STRIPE_PUBLISHABLE_KEY = "pk_test_placeholder"
STRIPE_SECRET_KEY = "sk_test_placeholder"
STRIPE_PRICE_OBJECT = "price_placeholder"
STRIPE_ENDPOINT_SECRET = "whsec_placeholder"

EMAIL_HOST = "smtp.example.com"
EMAIL_HOST_USER = "user@example.com"
EMAIL_HOST_PASSWORD = "placeholder"

ALLAUTH_GITHUB_CLIENT_ID = "placeholder"
ALLAUTH_GITHUB_SECRET = "placeholder"
ALLAUTH_GOOGLE_CLIENT_ID = "placeholder"
ALLAUTH_GOOGLE_SECRET = "placeholder"
EOF

export DATABASE_URL="postgresql://projectify@localhost/projectify"

uv sync --extra=postgresql
uv run ./manage.py check
