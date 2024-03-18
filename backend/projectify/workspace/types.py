# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Copyright (C) 2023 JWP Consulting GK
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Shared type definitions in workspace app."""
from dataclasses import dataclass
from typing import (
    Mapping,
    Optional,
    Sequence,
    TypedDict,
    Union,
)

from projectify.corporate.types import WorkspaceFeatures


class ConsumerEvent(TypedDict):
    """Contains event data about what to send to client."""

    type: str
    uuid: str


class Message(TypedDict):
    """Contains message to send to client."""

    type: str
    uuid: str
    # TODO Sequence required here?
    data: Optional[Union[Mapping[str, object], Sequence[object]]]


@dataclass(frozen=True, kw_only=True)
class Quota:
    """Store quota for a resource, including the maximum amount."""

    # None means irrelevant. No limit means counting unnecessary.
    current: Optional[int]
    # None means unlimited
    limit: Optional[int]
    can_create_more: bool


@dataclass(frozen=True, kw_only=True)
class WorkspaceQuota:
    """Contain all workspace quota values."""

    workspace_status: WorkspaceFeatures
    chat_messages: Quota
    labels: Quota
    sub_tasks: Quota
    tasks: Quota
    task_labels: Quota
    projects: Quota
    sections: Quota
    team_members_and_invites: Quota
