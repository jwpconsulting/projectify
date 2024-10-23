// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { error } from "@sveltejs/kit";

import { getWorkspace } from "$lib/repository/workspace/workspace";
import { getProject } from "$lib/repository/workspace/project";
import type { WorkspaceDetail, ProjectDetail } from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";

export async function load({
    params: { workspaceUuid },
}: PageLoadEvent): Promise<{
    workspace: WorkspaceDetail;
    project?: ProjectDetail;
}> {
    const workspace = await getWorkspace(workspaceUuid);
    if (!workspace) {
        error(404, `No workspace could be found for UUID '${workspaceUuid}'`);
    }
    const projectUuid = workspace.projects.at(0)?.uuid;
    const project = projectUuid ? await getProject(projectUuid) : undefined;
    return { workspace, project };
}
