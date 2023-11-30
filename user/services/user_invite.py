"""User invite services."""

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from user.models import UserInvite
from user.selectors.user import user_find_by_email


@transaction.atomic
def user_invite_create(*, email: str) -> UserInvite:
    """Invite a user by email address."""
    user = user_find_by_email(email=email)
    if user:
        # TODO make this return None instead
        raise ValueError(_("User already exists."))
    # TODO make this a selector
    invite_qs = UserInvite.objects.by_email(email).is_redeemed(False)
    if invite_qs.exists():
        return invite_qs.get()
    return UserInvite.objects.create(email=email)
