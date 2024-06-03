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
    postWithCredentialsJson,
    failOrOk,
    deleteWithCredentialsJson,
    openApiClient,
} from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type { components } from "$lib/types/schema";
import type {
    CreateUpdateSubTask,
    Label,
    Task,
    TaskDetail,
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
        labels: readonly Pick<Label, "uuid">[];
        // TODO this has to be optional in the backend -> undefined means unset
        // assignee
        assignee: Pick<TeamMember, "uuid"> | null;
        section: Pick<Section, "uuid">;
        // TODO dueDate plz
        due_date: string | null;
        sub_tasks: CreateUpdateSubTask[];
    },
    // TODO allow adding fetch reference here again
    // repositoryContext: RepositoryContext,
): Promise<TaskDetail> {
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
    task_uuid: string,
    _repositoryContext?: RepositoryContext,
): Promise<TaskDetail | undefined> {
    const { response, data } = await openApiClient.GET(
        "/workspace/task/{task_uuid}",
        { params: { path: { task_uuid } } },
    );
    if (response.ok) {
        return data;
    }
    if (response.status === 404) {
        return undefined;
    }
    throw new Error("uncaught");
}

// Update
// TODO change me to accept CreateOrUpdateTaskData directly
// Then we don't have to pass task, labels, ws user separately
// This is possible now because the API accepts a whole task object,
// incl. labels and so on
export async function updateTask(
    task: Pick<Task, "uuid">,
    updateData: {
        title: string;
        description: string | null;
        // TODO this has to be optional in the backend -> undefined means unset
        // labels
        labels: readonly Pick<Label, "uuid">[];
        // TODO this has to be optional in the backend -> undefined means unset
        // assignee
        assignee: Pick<TeamMember, "uuid"> | null;
        // TODO dueDate plz
        due_date: string | null;
        sub_tasks: readonly CreateUpdateSubTask[];
    },
    _repositoryContext?: RepositoryContext,
): Promise<components["schemas"]["TaskDetail"]> {
    const { uuid: task_uuid } = task;
    const body: components["schemas"]["TaskUpdate"] = {
        ...updateData,
        sub_tasks: [...updateData.sub_tasks],
        assignee: updateData.assignee
            ? { uuid: updateData.assignee.uuid }
            : null,
        labels: [
            ...updateData.labels.map((l) => {
                return { uuid: l.uuid };
            }),
        ],
    };
    const { data } = await openApiClient.PUT("/workspace/task/{task_uuid}", {
        params: { path: { task_uuid } },
        body,
    });
    if (data !== undefined) {
        return data;
    }
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
