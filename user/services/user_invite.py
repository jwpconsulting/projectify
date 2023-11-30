"""User invite services."""

from django.db import transaction
from django.utils.translation import gettext_lazy as _

from user import signal_defs
from user.models import User, UserInvite
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


def user_invite_redeem(*, user_invite: UserInvite, user: User) -> None:
    """Redeem a UserInvite."""
    assert not user_invite.redeemed
    user_invite.redeemed = True
    user_invite.user = user
    user_invite.save()
    signal_defs.user_invitation_redeemed.send(
        sender=user_invite.__class__,
        user=user,
        instance=user_invite,
    )


@transaction.atomic
def user_invite_redeem_many(*, user: User) -> None:
    """Redeem all invites for a user."""
    invites = UserInvite.objects.is_redeemed(False).by_email(user.email)
    for invitation in invites.iterator():
        user_invite_redeem(user_invite=invitation, user=user)
