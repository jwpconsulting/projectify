// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
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
import { error, redirect } from "@sveltejs/kit";

import { getWorkspace } from "$lib/repository/workspace/workspace";
import { getProject } from "$lib/repository/workspace/project";
import type { ProjectDetail, WorkspaceDetail } from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";
import { getLogInWithNextUrl } from "$lib/urls/user";
import type { User } from "$lib/types/user";

export async function load({
    params: { projectUuid },
    fetch,
    parent,
    url,
}: PageLoadEvent): Promise<{
    user: User;
    project: ProjectDetail;
    workspace: WorkspaceDetail;
    section?: ProjectDetail["sections"][number];
}> {
    const { userAwaitable } = await parent();
    const user = await userAwaitable;
    const project = await getProject(projectUuid, {
        fetch,
    });
    if (!project) {
        error(404, `No project could be found for UUID ${projectUuid}.`);
    }
    if (user.kind !== "authenticated") {
        redirect(302, getLogInWithNextUrl(url.pathname));
    }
    const { uuid: workspaceUuid } = project.workspace;
    const workspace = await getWorkspace(workspaceUuid, {
        fetch,
    });
    if (!workspace) {
        // If this happens something is very wrong
        error(
            500,
            `No workspace with UUID ${workspaceUuid} could be found for project UUID ${projectUuid}.`,
        );
    }
    const section = project.sections.at(0);
    return { user, project, workspace, section };
}
