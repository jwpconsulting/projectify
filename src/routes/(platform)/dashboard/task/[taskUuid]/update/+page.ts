import { currentWorkspaceUuid } from "$lib/stores/dashboard";

import { getTask } from "$lib/repository/workspace";
import type { Task } from "$lib/types/workspace";

export const prerender = false;
export const ssr = false;

export async function load({
    params: { taskUuid },
    fetch,
}: {
    params: { taskUuid: string };
    fetch: typeof window.fetch;
}): Promise<{ task: Task }> {
    const task = await getTask(taskUuid, { fetch });
    const { workspace_board_section } = task;
    if (!workspace_board_section) {
        throw new Error("Expected workspace_board_section");
    }
    const { workspace_board } = workspace_board_section;
    if (!workspace_board) {
        throw new Error("Expected workspace_board");
    }
    const { workspace } = workspace_board;
    if (!workspace) {
        throw new Error("Expected workspace");
    }
    currentWorkspaceUuid.set(workspace.uuid);
    return { task };
}
