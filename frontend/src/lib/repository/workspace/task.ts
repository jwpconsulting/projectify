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
import {
    putWithCredentialsJson,
    getWithCredentialsJson,
    postWithCredentialsJson,
    handle404,
    failOrOk,
    deleteWithCredentialsJson,
    openApiClient,
} from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type {
    CreateUpdateSubTask,
    Label,
    Task,
    TaskWithWorkspace,
    Section,
    TeamMember,
} from "$lib/types/workspace";

// Task CRUD
// Create

export async function createTask(
    data: {
        title: string;
        description: string | null;
        // TODO this has to be optional in the backend -> undefined means unset
        // labels
        labels: Pick<Label, "uuid">[];
        // TODO this has to be optional in the backend -> undefined means unset
        // assignee
        assignee?: Pick<TeamMember, "uuid">;
        section: Pick<Section, "uuid">;
        // TODO dueDate plz
        due_date: string | null;
        sub_tasks?: CreateUpdateSubTask[];
    },
    // TODO allow adding fetch reference here again
    // repositoryContext: RepositoryContext,
): Promise<Task> {
    const body = {
        ...data,
        section: {
            uuid: data.section.uuid,
        },
        labels: data.labels.map((l) => {
            return { uuid: l.uuid };
        }),
        assignee: data.assignee ? { uuid: data.assignee.uuid } : null,
    };
    const { data: content, response } = await openApiClient.POST(
        "/workspace/task/",
        {
            body,
        },
    );
    if (response.status === 400) {
        // TODO show the user what the bad request was
        throw new Error("400 encountered");
    }
    if (content === undefined) {
        throw new Error("Other error encountered");
    }
    return content;
}

// Read
export async function getTask(
    uuid: string,
    repositoryContext: RepositoryContext,
): Promise<TaskWithWorkspace | undefined> {
    return handle404(
        await getWithCredentialsJson<TaskWithWorkspace>(
            `/workspace/task/${uuid}`,
            repositoryContext,
        ),
    );
}

// Update
// TODO change me to accept CreateOrUpdateTaskData directly
// Then we don't have to pass task, labels, ws user separately
// This is possible now because the API accepts a whole task object,
// incl. labels and so on
export async function updateTask(
    task: Pick<Task, "uuid">,
    data: {
        title: string;
        description: string | null;
        // TODO this has to be optional in the backend -> undefined means unset
        // labels
        labels: readonly Pick<Label, "uuid">[];
        // TODO this has to be optional in the backend -> undefined means unset
        // assignee
        assignee?: Pick<TeamMember, "uuid">;
        // TODO dueDate plz
        due_date: string | null;
        sub_tasks?: readonly CreateUpdateSubTask[];
    },
    repositoryContext: RepositoryContext,
): Promise<Task | undefined> {
    const { uuid } = task;
    const response = await putWithCredentialsJson<Task>(
        `/workspace/task/${uuid}`,
        {
            ...data,
            assignee: data.assignee ? { uuid: data.assignee.uuid } : null,
            labels: data.labels.map((l) => {
                return { uuid: l.uuid };
            }),
        },
        repositoryContext,
    );
    if (response.ok) {
        return response.data;
    } else if (response.kind === "badRequest") {
        // TODO handle 400
        console.error("Bad request");
    }
    console.error(response.error);
    throw new Error();
}

export async function moveTaskToSection(
    task: Pick<Task, "uuid">,
    { uuid }: Pick<Section, "uuid">,
    repositoryContext: RepositoryContext,
): Promise<void> {
    failOrOk(
        await postWithCredentialsJson(
            `/workspace/task/${task.uuid}/move-to-section`,
            { section_uuid: uuid },
            repositoryContext,
        ),
    );
}

export async function moveTaskAfterTask(
    task: Pick<Task, "uuid">,
    { uuid }: Pick<Task, "uuid">,
    repositoryContext: RepositoryContext,
): Promise<void> {
    failOrOk(
        await postWithCredentialsJson(
            `/workspace/task/${task.uuid}/move-after-task`,
            { task_uuid: uuid },
            repositoryContext,
        ),
    );
}

// Delete
export async function deleteTask(task: Pick<Task, "uuid">): Promise<void> {
    failOrOk(
        await deleteWithCredentialsJson(`/workspace/task/${task.uuid}`, {
            fetch,
        }),
    );
}
