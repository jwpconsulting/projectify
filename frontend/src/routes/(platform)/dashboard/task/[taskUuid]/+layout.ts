// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { currentTask } from "$lib/stores/dashboard/task";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { TaskDetail } from "$lib/types/workspace";

import type { LayoutLoadEvent } from "./$types";

interface Data {
    task: Promise<TaskDetail>;
}

export function load({ params: { taskUuid } }: LayoutLoadEvent): Data {
    // TODO add back
    // if (!task) {
    //     error(404, `No task could be found for UUID '${taskUuid}'`);
    // }
    const task = currentTask
        .loadUuid(taskUuid)
        .then((task) => {
            if (!task) {
                throw new Error(
                    `No task could be found for UUID '${taskUuid}'`,
                );
            }
            return task;
        })
        .then((task) => {
            currentWorkspace
                .loadUuid(task.section.project.workspace.uuid)
                .catch((error: unknown) =>
                    console.error(
                        "Error when fetching currentWorkspace for task ${taskUuid}",
                        error,
                    ),
                );
            return task;
        });
    return { task };
}
export const prerender = false;
// TODO Maybe we can set this to true at some point and have SSR support
export const ssr = false;
