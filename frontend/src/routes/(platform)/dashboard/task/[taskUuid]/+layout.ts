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
import { currentTask, currentWorkspace } from "$lib/stores/dashboard";
import type { TaskWithWorkspace } from "$lib/types/workspace";

import type { LayoutLoadEvent } from "./$types";

interface Data {
    task: Promise<TaskWithWorkspace>;
}

export function load({ params: { taskUuid }, fetch }: LayoutLoadEvent): Data {
    // TODO add back
    // if (!task) {
    //     error(404, `No task could be found for UUID '${taskUuid}'`);
    // }
    const task = currentTask
        .loadUuid(taskUuid, { fetch })
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
                .loadUuid(task.section.project.workspace.uuid, { fetch })
                .catch((error) =>
                    console.error(
                        `Error when fetching currentWorkspace for task ${taskUuid}: ${error}`,
                    ),
                );
            return task;
        });
    return { task };
}
