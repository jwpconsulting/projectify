# flake8: noqa: F401, F403
from .base import *


SECRET_KEY = "test"

STATIC_ROOT = None

FRONTEND_URL = "https://example.com"

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_EAGER = True

# GraphQL
GRAPHIQL_ENABLE = False  #

# Stripe
STRIPE_SECRET_KEY = "null"
STRIPE_ENDPOINT_SECRET = "null"
