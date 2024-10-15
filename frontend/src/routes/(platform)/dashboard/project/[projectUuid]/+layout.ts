// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
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
