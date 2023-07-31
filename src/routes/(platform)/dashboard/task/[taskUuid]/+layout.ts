import type { LayoutLoadEvent } from "./$types";

import {
    currentTask,
    currentWorkspaceUuid,
    currentTaskUuid,
} from "$lib/stores/dashboard";

export const prerender = false;
export const ssr = false;

export function load({ params: { taskUuid } }: LayoutLoadEvent) {
    // XXX Ideally we would already have set an instance of the task here,
    // then inside +page.svelte we would not have a nullable Task
    // XXX perhaps we can even init taskModule here
    currentTaskUuid.set(taskUuid);

    currentTask.subscribe(($currentTask) => {
        if (!$currentTask) {
            return;
        }
        const { workspace_board_section } = $currentTask;
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
    });
}
