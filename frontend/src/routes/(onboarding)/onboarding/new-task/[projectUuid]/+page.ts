// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { error, redirect } from "@sveltejs/kit";

import { getWorkspace } from "$lib/repository/workspace/workspace";
import { getProject } from "$lib/repository/workspace/project";
import type { ProjectDetail, WorkspaceDetail } from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";
import { getLogInWithNextUrl } from "$lib/urls/user";
import type { User } from "$lib/types/user";

export async function load({
    params: { projectUuid },
    parent,
    url,
}: PageLoadEvent): Promise<{
    user: User;
    project: ProjectDetail;
    workspace: WorkspaceDetail;
    section?: ProjectDetail["sections"][number];
}> {
    const { user } = await parent();
    const project = await getProject(projectUuid);
    if (!project) {
        error(404, `No project could be found for UUID ${projectUuid}.`);
    }
    if (user.kind !== "authenticated") {
        redirect(302, getLogInWithNextUrl(url.pathname));
    }
    const { uuid: workspaceUuid } = project.workspace;
    const workspace = await getWorkspace(workspaceUuid);
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
