import type { Unsubscriber } from "svelte/store";

import type { LayoutLoadEvent } from "./$types";

import {
    currentTask,
    currentTaskUuid,
    currentWorkspace,
} from "$lib/stores/dashboard";
import type {
    Task,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
} from "$lib/types/workspace";

export const prerender = false;
export const ssr = false;

interface Data {
    task: Task;
    workspaceBoardSection: WorkspaceBoardSection;
    workspaceBoard: WorkspaceBoard;
    workspace: Workspace;
}

export async function load({
    params: { taskUuid },
}: LayoutLoadEvent): Promise<Data> {
    let unsubscriber: Unsubscriber | undefined = undefined;
    const data = new Promise<Data>((resolve) => {
        // Retrieving the data for this page through a subscription is weird
        unsubscriber = currentTask.subscribe(async ($currentTask) => {
            if (!$currentTask) {
                return;
            }
            const { workspace_board_section: workspaceBoardSection } =
                $currentTask;
            if (!workspaceBoardSection) {
                throw new Error("Expected workspace_board_section");
            }
            const { workspace_board: workspaceBoard } = workspaceBoardSection;
            if (!workspaceBoard) {
                throw new Error("Expected workspace_board");
            }
            const workspaceUuid = workspaceBoard.workspace?.uuid;
            if (!workspaceUuid) {
                throw new Error("Expected workspaceUuid");
            }
            const workspace = await currentWorkspace.loadUuid(workspaceUuid);
            resolve({
                task: $currentTask,
                workspaceBoardSection,
                workspaceBoard,
                workspace,
            });
            // I don't see a world where unsubscriber wouldn't be assigned, but
            // we never know...
            if (!unsubscriber) {
                throw new Error("Expected unsubscriber");
            }
            // Sometimes we forget to unsubscribe
            unsubscriber();
        });
    });
    currentTaskUuid.set(taskUuid);
    return await data;
}
