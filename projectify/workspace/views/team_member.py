# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2026 JWP Consulting GK
"""Team member views."""

import logging
from uuid import UUID

from django.http import Http404, HttpResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods

from django_sendfile import sendfile

from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view

from ..selectors.team_member import team_member_find_by_team_member_uuid

logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
@platform_view
def team_member_picture(
    request: AuthenticatedHttpRequest, team_member_uuid: UUID
) -> HttpResponse:
    """Return picture for a team member."""
    team_member = team_member_find_by_team_member_uuid(
        who=request.user, team_member_uuid=team_member_uuid
    )
    if not team_member:
        raise Http404(_("Team member not found"))
    if not team_member.user.profile_picture:
        logger.warning(
            "No picture available for team member %s", team_member_uuid
        )
        raise Http404(_("No picture available"))
    return sendfile(request, team_member.user.profile_picture.path)
