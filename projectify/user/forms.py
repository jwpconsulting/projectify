# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Forms for user app."""

from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.forms import SignupForm


class SocialAccountSignUpForm(SignupForm):
    """Sign up form for social accounts."""

    tos_agreed = forms.BooleanField()
    privacy_policy_agreed = forms.BooleanField()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Hide email field."""
        super().__init__(*args, **kwargs)  # type: ignore[no-untyped-call]
        self.fields["email"].widget = forms.HiddenInput()

    # XXX quite the hack
    def clean_email(self) -> Any:
        """Make sure user can't mess with readonly."""
        data: str = self.cleaned_data["email"]
        initial = get_adapter().get_signup_form_initial_data(self.sociallogin)  # type: ignore[no-untyped-call]
        initial_email = initial.get("email")
        if initial_email and data != initial_email:
            raise ValidationError(
                _("Email must be: {email}").format(email=initial_email)
            )
        return super().clean_email()  # type: ignore[no-untyped-call]
