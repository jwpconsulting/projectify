import { error } from "@sveltejs/kit";

import { currentTask } from "$lib/stores/dashboard";
import type {
    Label,
    Task,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
    WorkspaceUser,
} from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

import type { PageLoadEvent } from "./$types";

interface returnType {
    task: Task;
    workspaceBoardSection: WorkspaceBoardSection;
    workspaceBoard: WorkspaceBoard;
    workspace: Workspace;
    label: Label;
    assignee: WorkspaceUser;
}
export async function load({
    fetch,
    params: { taskUuid },
}: PageLoadEvent): Promise<returnType> {
    const task = await currentTask.loadUuid(taskUuid, { fetch });
    if (!task) {
        throw error(404);
    }
    const workspaceBoardSection = task.workspace_board_section;
    const workspaceBoard = workspaceBoardSection.workspace_board;
    const { workspace } = workspaceBoard;
    const label = unwrap(task.labels.at(0), "Expected label");
    const assignee = unwrap(task.assignee, "Expected assignee");
    return {
        task,
        assignee,
        workspaceBoardSection,
        workspaceBoard,
        workspace,
        label,
    };
}
