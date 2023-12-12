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
    CreateUpdateTask,
    Label,
    Task,
    TaskWithWorkspace,
    WorkspaceBoardSection,
    WorkspaceUser,
} from "$lib/types/workspace";

// Task CRUD
// Create
interface CreateUpdateTaskData {
    title: string;
    description?: string;
    // TODO this has to be optional in the backend -> undefined means unset
    // labels
    labels: Label[];
    // TODO this has to be optional in the backend -> undefined means unset
    // assignee
    assignee: WorkspaceUser | null;
    workspace_board_section: WorkspaceBoardSection;
    // TODO dueDate plz
    deadline?: string;
    sub_tasks?: CreateUpdateSubTask[];
}
// TODO change me to accept CreateOrUpdateTaskData directly
export async function createTask(
    createTask: CreateUpdateTask,
    repositoryContext: RepositoryContext
): Promise<Task> {
    const data: CreateUpdateTaskData = {
        ...createTask,
        // TODO: Should the API just accept a missing value here?
        assignee: createTask.assignee ?? null,
    };
    const response = await postWithCredentialsJson<Task>(
        "/workspace/task/",
        data,
        repositoryContext
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
    repositoryContext: RepositoryContext
): Promise<TaskWithWorkspace | undefined> {
    return handle404(
        await getWithCredentialsJson<TaskWithWorkspace>(
            `/workspace/task/${uuid}`,
            repositoryContext
        )
    );
}

// Update
// TODO change me to accept CreateOrUpdateTaskData directly
// Then we don't have to pass task, labels, ws user separately
// This is possible now because the API accepts a whole task object,
// incl. labels and so on
export async function updateTask(
    task: Task & {
        workspace_board_section: Pick<WorkspaceBoardSection, "uuid">;
    },
    // XXX please move the following three arguments back into the top task
    // argument
    labels: Label[],
    workspaceUser: WorkspaceUser | undefined,
    subTasks: CreateUpdateSubTask[] | undefined,
    repositoryContext: RepositoryContext
): Promise<Task | undefined> {
    const { uuid } = task;
    const data: CreateUpdateTaskData = {
        title: task.title,
        description: task.description ?? undefined,
        deadline: task.deadline,
        // XXX
        // Ideally, the two following arguments would just be part of the Task
        labels,
        // TODO
        // Please be undefined, not null
        // Might have to check if the backend already accepts undefined as
        // unassign
        assignee: workspaceUser ?? null,
        workspace_board_section: task.workspace_board_section,
        sub_tasks: subTasks,
    };
    const response = await putWithCredentialsJson<Task>(
        `/workspace/task/${uuid}`,
        data,
        repositoryContext
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
    repositoryContext: RepositoryContext
): Promise<void> {
    failOrOk(
        await postWithCredentialsJson(
            `/workspace/task/${task.uuid}/move-to-workspace-board-section`,
            { workspace_board_section_uuid: uuid },
            repositoryContext
        )
    );
}

export async function moveTaskAfterTask(
    task: Task,
    { uuid }: Task,
    repositoryContext: RepositoryContext
): Promise<void> {
    failOrOk(
        await postWithCredentialsJson(
            `/workspace/task/${task.uuid}/move-after-task`,
            { task_uuid: uuid },
            repositoryContext
        )
    );
}

// Delete
export async function deleteTask(task: Task): Promise<void> {
    failOrOk(
        await deleteWithCredentialsJson(`/workspace/task/${task.uuid}`, {
            fetch,
        })
    );
}
