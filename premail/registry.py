"""Premail email registry."""
import importlib
import inspect

from django.apps import (
    apps,
)

from .email import (
    TemplateEmail,
)


registry = {
    # 'user-email-confirmation': user_emails.UserEmailConfirmationEmail,
}


def add_members(emails: object) -> None:
    """Add email templates to registry."""
    for name, obj in inspect.getmembers(emails):
        is_candidate = (
            inspect.isclass(obj)
            and obj is not TemplateEmail
            and issubclass(obj, TemplateEmail)
        )
        if is_candidate:
            registry[name] = obj


for app in apps.app_configs:
    try:
        emails = importlib.import_module(f"{app}.emails")
    except ModuleNotFoundError:
        continue
    add_members(emails)
