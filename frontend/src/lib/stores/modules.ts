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
// TODO consider putting this either in repository or make it part of the
// task store file
import { openApiClient } from "$lib/repository/util";
import type {
    Task,
    SectionWithTasks,
    ProjectDetailTask,
    Section,
} from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

type TaskPosition =
    | { kind: "top"; position: 0; isOnly: boolean }
    | { kind: "within"; position: number; isOnly: false }
    | { kind: "bottom"; position: number; isOnly: false }
    | { kind: "outside"; isOnly: undefined };

function getTaskPosition(
    section: SectionWithTasks,
    task: Pick<Task, "uuid">,
): TaskPosition {
    const { tasks } = section;
    const taskIndex = tasks.findIndex((t) => t.uuid == task.uuid);
    const lastIndex = tasks.length - 1;
    switch (taskIndex) {
        case -1:
            return { kind: "outside", isOnly: undefined };
        case 0:
            return { kind: "top", position: 0, isOnly: tasks.length === 1 };
        case lastIndex:
            return { kind: "bottom", position: lastIndex, isOnly: false };
        default:
            return { kind: "within", position: taskIndex, isOnly: false };
    }
}

async function moveTaskAfterTask(
    task: Pick<Task, "uuid">,
    { uuid }: Pick<Task, "uuid">,
): Promise<void> {
    const { error } = await openApiClient.POST(
        "/workspace/task/{task_uuid}/move-after-task",
        {
            params: { path: { task_uuid: task.uuid } },
            body: { task_uuid: uuid },
        },
    );
    if (error === undefined) {
        return;
    }
    throw new Error("Could not move task after task");
}

async function moveToBottom(
    section: SectionWithTasks,
    task: Pick<Task, "uuid">,
) {
    const { tasks } = section;
    const lastTask = tasks[tasks.length - 1];
    if (lastTask === undefined) {
        throw new Error("Expected lastTask");
    }
    await moveTaskAfterTask(task, lastTask);
}

async function moveUp(
    section: SectionWithTasks,
    task: Pick<ProjectDetailTask, "uuid">,
) {
    const { tasks } = section;
    const position = getTaskPosition(section, task);
    if (!(position.kind === "within" || position.kind === "bottom")) {
        throw new Error("Expected task to be within or at bottom");
    }
    const prevTask = unwrap(
        tasks.at(position.position - 1),
        "Expected prevTask",
    );
    await moveTaskAfterTask(task, prevTask);
}

async function moveDown(
    section: SectionWithTasks,
    task: Pick<ProjectDetailTask, "uuid">,
) {
    const position = getTaskPosition(section, task);
    if (!(position.kind === "top" || position.kind === "within")) {
        throw new Error("Expected task to be at top or within");
    }
    const tasks = unwrap(section.tasks, "Expected tasks");
    const nextTask = unwrap(
        tasks.at(position.position + 1),
        "Expected nextTask",
    );
    await moveTaskAfterTask(task, nextTask);
}

async function moveTaskToSection(
    { uuid }: Pick<Section, "uuid">,
    task: Pick<Task, "uuid">,
): Promise<void> {
    const { error } = await openApiClient.POST(
        "/workspace/task/{task_uuid}/move-to-section",
        {
            params: { path: { task_uuid: task.uuid } },
            body: { section_uuid: uuid },
        },
    );
    if (error === undefined) {
        return;
    }
    throw new Error("Could not move task to section");
}

type MoveTaskWhere =
    | { kind: "top"; section: SectionWithTasks }
    | { kind: "up"; section: SectionWithTasks }
    | { kind: "down"; section: SectionWithTasks }
    | { kind: "bottom"; section: SectionWithTasks }
    | { kind: "section"; section: SectionWithTasks };

export function canMoveTask(
    task: Pick<Task, "uuid">,
    { kind, section }: MoveTaskWhere,
) {
    if (kind === "section") {
        return true;
    }
    const pos = getTaskPosition(section, task);
    if (pos.isOnly) {
        return false;
    }
    switch (kind) {
        case "top":
        case "up":
            return pos.kind !== "top";
        case "down":
        case "bottom":
            return pos.kind !== "bottom";
    }
}

export async function moveTask(
    task: Pick<Task, "uuid">,
    { kind, section }: MoveTaskWhere,
) {
    switch (kind) {
        case "top":
            return await moveTaskToSection(section, task);
        case "up":
            return await moveUp(section, task);
        case "down":
            return await moveDown(section, task);
        case "bottom":
            return await moveToBottom(section, task);
        case "section":
            return await moveTaskToSection(section, task);
    }
}
