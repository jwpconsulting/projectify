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
import type { ProjectDetail } from "$lib/types/workspace";
import { dashboardUrl } from "$lib/urls/dashboard";

import type { LayoutLoadEvent } from "./$types";

import { goto } from "$app/navigation";
import { currentProject } from "$lib/stores/dashboard/project";

interface Data {
    project: Promise<ProjectDetail | undefined>;
}

export function load({ params: { projectUuid } }: LayoutLoadEvent): Data {
    const project: Promise<ProjectDetail | undefined> = currentProject
        .loadUuid(projectUuid)
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
        .catch(async () => {
            await goto(dashboardUrl);
            return undefined;
        });
    return { project };
}

export const prerender = false;
// TODO Maybe we can set this to true at some point and have SSR support
export const ssr = false;
