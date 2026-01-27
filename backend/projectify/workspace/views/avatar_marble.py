# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023-2026 JWP Consulting GK
# SPDX-FileCopyrightText: 2023 paolotiu
# Original idea from https://boringavatars.com/
"""Avatar marble view."""

from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

from django.http import Http404, HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

from projectify.lib.types import AuthenticatedHttpRequest
from projectify.lib.views import platform_view
from projectify.workspace.selectors.team_member import (
    team_member_find_by_team_member_uuid,
)


@dataclass
class MarbleColor:
    """Represents a color configuration for marble avatar."""

    color: str
    translate_x: float
    translate_y: float
    scale: float
    rotate: float


def _get_unit(
    number: int, range_val: int, index: Optional[int] = None
) -> float:
    """Get a unit value with optional negation based on digit parity."""
    value = number % range_val
    if index and (number // (10**index)) % 2 == 0:
        return -value
    return value


COLORS = "#92A1C6", "#146A7C", "#F0AB3D", "#C271B4", "#C20D90"


def _generate_marble_colors(name: str, size: int) -> List[MarbleColor]:
    """Generate three marble colors with transforms for the given name."""
    num_from_name = sum(ord(char) for char in name)

    return [
        MarbleColor(
            color=COLORS[(num_from_name + i) % len(COLORS)],
            translate_x=_get_unit(num_from_name * (i + 1), size // 10, 1),
            translate_y=_get_unit(num_from_name * (i + 1), size // 10, 2),
            scale=1.2 + _get_unit(num_from_name * (i + 1), size // 20) / 10,
            rotate=_get_unit(num_from_name * (i + 1), 360, 1),
        )
        for i in range(3)
    ]


@platform_view
@require_GET
@cache_control(max_age=3600)
def avatar_marble_view(
    request: AuthenticatedHttpRequest, team_member_uuid: UUID
) -> HttpResponse:
    """Generate and return a marble avatar SVG."""
    team_member = team_member_find_by_team_member_uuid(
        who=request.user, team_member_uuid=team_member_uuid
    )
    if team_member is None:
        raise Http404("Team member with this UUID not found")
    uuid = str(team_member.uuid)
    # Get query parameters
    size = 80

    name_hash = abs(hash(uuid))
    mask_id = f"mask__marble__{name_hash}"
    filter_id = f"prefix__filter0_f__{name_hash}"

    marble_colors = _generate_marble_colors(uuid, 80)

    svg_content = render_to_string(
        "workspace/avatar_marble.svg",
        {
            "size": size,
            "title": str(team_member.user),
            "mask_id": mask_id,
            "filter_id": filter_id,
            "marble_colors": marble_colors,
        },
    )

    return HttpResponse(svg_content, content_type="image/svg+xml")
