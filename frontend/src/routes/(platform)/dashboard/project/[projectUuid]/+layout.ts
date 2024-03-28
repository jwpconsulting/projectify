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
import { currentWorkspace, currentProject } from "$lib/stores/dashboard";
import type { ProjectDetail } from "$lib/types/workspace";
import { dashboardUrl } from "$lib/urls/dashboard";

import type { LayoutLoadEvent } from "./$types";

import { goto } from "$app/navigation";

interface Data {
    project: Promise<ProjectDetail | undefined>;
}

export function load({
    params: { projectUuid },
    fetch,
}: LayoutLoadEvent): Data {
    const project: Promise<ProjectDetail | undefined> = currentProject
        .loadUuid(projectUuid, { fetch })
        .then((project) => {
            if (!project) {
                // If we don't have a project, we don't have anything (no
                // workspace uuid etc), so we are back to the dashboard in that case.
                // TODO tell the user that we have done so
                throw new Error(
                    `No project could be found for UUID '${projectUuid}'`,
                );
            }
            return project;
        })
        .then((project) => {
            const workspaceUuid = project.workspace.uuid;
            currentWorkspace
                .loadUuid(workspaceUuid, {
                    fetch,
                })
                .then((workspace) => {
                    if (!workspace) {
                        throw new Error(
                            `For project ${projectUuid}, the workspace with UUID ${workspaceUuid} could not be found.`,
                        );
                    }
                })
                .catch((error) =>
                    console.error(
                        `Something went very wrong when fetching workspace ${workspaceUuid}: ${error}`,
                    ),
                );
            return project;
        })
        .catch(async () => {
            await goto(dashboardUrl);
            return undefined;
        });
    return { project };
}
