// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { currentTask } from "$lib/stores/dashboard/task";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { TaskDetail } from "$lib/types/workspace";
import { error } from "@sveltejs/kit";

import type { LayoutLoadEvent } from "./$types";

interface Data {
    task: TaskDetail;
}

export async function load({
    params: { taskUuid },
}: LayoutLoadEvent): Promise<Data> {
    const task = await currentTask.loadUuid(taskUuid);
    if (!task) {
        error(404, `No task could be found for UUID '${taskUuid}'`);
    }
    currentWorkspace
        .loadUuid(task.section.project.workspace.uuid)
        .catch((error: unknown) =>
            console.error(
                "Error when fetching currentWorkspace for task ${taskUuid}",
                error,
            ),
        );
    return { task };
}
export const prerender = false;
