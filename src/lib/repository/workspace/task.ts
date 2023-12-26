import {
    putWithCredentialsJson,
    getWithCredentialsJson,
    postWithCredentialsJson,
    handle404,
    failOrOk,
    deleteWithCredentialsJson,
} from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type {
    CreateUpdateSubTask,
    Label,
    Task,
    TaskWithWorkspace,
    WorkspaceBoardSection,
    WorkspaceUser,
} from "$lib/types/workspace";

// Task CRUD
// Create
export interface CreateUpdateTaskData {
    title: string;
    description?: string;
    // TODO this has to be optional in the backend -> undefined means unset
    // labels
    labels: Pick<Label, "uuid">[];
    // TODO this has to be optional in the backend -> undefined means unset
    // assignee
    assignee?: Pick<WorkspaceUser, "uuid">;
    workspace_board_section: Pick<WorkspaceBoardSection, "uuid">;
    // TODO dueDate plz
    deadline?: string;
    sub_tasks?: CreateUpdateSubTask[];
}

export async function createTask(
    data: CreateUpdateTaskData,
    repositoryContext: RepositoryContext,
): Promise<Task> {
    const response = await postWithCredentialsJson<Task>(
        "/workspace/task/",
        {
            ...data,
            workspace_board_section: {
                uuid: data.workspace_board_section.uuid,
            },
            labels: data.labels.map((l) => {
                return { uuid: l.uuid };
            }),
            assignee: data.assignee ? { uuid: data.assignee.uuid } : null,
        },
        repositoryContext,
    );
    if (response.ok) {
        return response.data;
    } else if (response.kind === "badRequest") {
        // TODO show the user what the bad request was
        console.error(response.error);
    }
    throw new Error("Don't know how to handle this");
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
    data: CreateUpdateTaskData,
    repositoryContext: RepositoryContext,
): Promise<Task | undefined> {
    const { uuid } = task;
    const response = await putWithCredentialsJson<Task>(
        `/workspace/task/${uuid}`,
        {
            ...data,
            workspace_board_section: {
                uuid: data.workspace_board_section.uuid,
            },
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

export async function moveTaskToWorkspaceBoardSection(
    task: Task,
    { uuid }: WorkspaceBoardSection,
    repositoryContext: RepositoryContext,
): Promise<void> {
    failOrOk(
        await postWithCredentialsJson(
            `/workspace/task/${task.uuid}/move-to-workspace-board-section`,
            { workspace_board_section_uuid: uuid },
            repositoryContext,
        ),
    );
}

export async function moveTaskAfterTask(
    task: Task,
    { uuid }: Task,
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
export async function deleteTask(task: Task): Promise<void> {
    failOrOk(
        await deleteWithCredentialsJson(`/workspace/task/${task.uuid}`, {
            fetch,
        }),
    );
}
