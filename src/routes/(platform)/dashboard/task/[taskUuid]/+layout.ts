import { currentTask, currentWorkspace } from "$lib/stores/dashboard";
import type { TaskWithWorkspace, Workspace } from "$lib/types/workspace";

import type { LayoutLoadEvent } from "./$types";

interface Data {
    task: TaskWithWorkspace;
    workspace: Workspace;
}

export async function load({
    params: { taskUuid },
}: LayoutLoadEvent): Promise<Data> {
    const task = await currentTask.loadUuid(taskUuid);
    const workspace = await currentWorkspace.loadUuid(
        task.workspace_board_section.workspace_board.workspace.uuid
    );
    return {
        task,
        workspace,
    };
}
