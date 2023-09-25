"""Contains enums and other constant values."""
from django.db import (
    models,
)
from django.utils.translation import gettext_lazy as _


class WorkspaceUserRoles(models.TextChoices):
    """Roles available."""

    OBSERVER = "OBSERVER", _("Observer")
    MEMBER = "MEMBER", _("Member")
    MAINTAINER = "MAINTAINER", _("Maintainer")
    OWNER = "OWNER", _("Owner")


OBSERVER_EQUIVALENT = [
    WorkspaceUserRoles.OBSERVER,
    WorkspaceUserRoles.MEMBER,
    WorkspaceUserRoles.MAINTAINER,
    WorkspaceUserRoles.OWNER,
]
MEMBER_EQUIVALENT = [
    WorkspaceUserRoles.MEMBER,
    WorkspaceUserRoles.MAINTAINER,
    WorkspaceUserRoles.OWNER,
]
MAINTAINER_EQUIVALENT = [
    WorkspaceUserRoles.MAINTAINER,
    WorkspaceUserRoles.OWNER,
]
OWNER_EQUIVALENT = [
    WorkspaceUserRoles.OWNER,
]
