# SPDX-License-Identifier: AGPL-3.0-or-later
#
# SPDX-FileCopyrightText: 2023 JWP Consulting GK
"""Shared type definitions in workspace app."""

from dataclasses import dataclass
from typing import Literal, Optional, TypedDict

from projectify.corporate.types import WorkspaceFeatures


class ConsumerEvent(TypedDict):
    """Contains event data about what to send to client."""

    type: Literal["change"]
    resource: Literal["workspace", "project", "task"]
    uuid: str
    kind: Literal["changed", "gone"]


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
    tasks: Quota
    task_labels: Quota
    projects: Quota
    sections: Quota
    team_members_and_invites: Quota


Resource = Literal["workspace", "project", "task"]
