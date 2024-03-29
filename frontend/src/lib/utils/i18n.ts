// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023-2024 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import type { TeamMemberRole } from "$lib/types/teamMemberRole";

export function getMessageNameForRole(
    $_: (id: string) => string,
    role: TeamMemberRole,
) {
    return {
        OBSERVER: $_("roles.observer"),
        CONTRIBUTOR: $_("roles.contributor"),
        MAINTAINER: $_("roles.maintainer"),
        OWNER: $_("roles.owner"),
    }[role];
}

interface HelpTopic {
    title: string;
    description: string;
    href: string;
    isOverview?: boolean;
}

export function helpTopics($_: (id: string) => string): HelpTopic[] {
    return [
        {
            title: $_("help.overview"),
            description: "",
            href: "/help",
            isOverview: true,
        },
        {
            title: $_("help.basics.title"),
            description: $_("help.basics.description"),
            href: "/help/basics",
        },
        {
            title: $_("help.workspaces.title"),
            description: $_("help.workspaces.description"),
            href: "/help/workspaces",
        },
        {
            title: $_("help.projects.title"),
            description: $_("help.projects.description"),
            href: "/help/projects",
        },
        {
            title: $_("help.sections.title"),
            description: $_("help.sections.description"),
            href: "/help/sections",
        },
        {
            title: $_("help.tasks.title"),
            description: $_("help.tasks.description"),
            href: "/help/tasks",
        },
        {
            title: $_("help.labels.title"),
            description: $_("help.labels.description"),
            href: "/help/labels",
        },
        {
            title: $_("help.team-members.title"),
            description: $_("help.team-members.description"),
            href: "/help/team-members",
        },
        {
            title: $_("help.filters.title"),
            description: $_("help.filters.description"),
            href: "/help/filters",
        },
        {
            title: $_("help.billing.title"),
            description: $_("help.billing.description"),
            href: "/help/billing",
        },
        {
            title: $_("help.trial.title"),
            description: $_("help.trial.description"),
            href: "/help/trial",
        },
        {
            title: $_("help.quota.title"),
            description: $_("help.quota.description"),
            href: "/help/quota",
        },
        {
            title: $_("help.roles.title"),
            description: $_("help.roles.description"),
            href: "/help/roles",
        },
    ] satisfies HelpTopic[];
}
