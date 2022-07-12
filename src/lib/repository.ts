import vars from "$lib/env";
import type {
    User,
    WorkspaceBoard,
    Workspace,
    Customer,
    Task,
} from "$lib/types";

export async function getUser(): Promise<User> {
    const response = await fetch(`${vars.API_ENDPOINT}/user/user`, {
        credentials: "include",
    });
    return await response.json();
}

export async function getWorkspaceBoard(
    uuid: string
): Promise<WorkspaceBoard> {
    const response = await fetch(
        `${vars.API_ENDPOINT}/workspace/workspace-board/${uuid}`,
        { credentials: "include" }
    );
    return await response.json();
}

export async function getWorkspaces(): Promise<Workspace[]> {
    const response = await fetch(
        `${vars.API_ENDPOINT}/workspace/user/workspaces/`,
        { credentials: "include" }
    );
    return await response.json();
}

export async function getWorkspace(uuid: string): Promise<Workspace> {
    const response = await fetch(
        `${vars.API_ENDPOINT}/workspace/workspace/${uuid}`,
        { credentials: "include" }
    );
    return await response.json();
}

export async function getTask(uuid: string): Promise<Task> {
    const response = await fetch(
        `${vars.API_ENDPOINT}/workspace/task/${uuid}`,
        { credentials: "include" }
    );
    return await response.json();
}

export async function getArchivedWorkspaceBoards(
    workspace_uuid: string
): Promise<WorkspaceBoard[]> {
    const response = await fetch(
        `${vars.API_ENDPOINT}/workspace/workspace/${workspace_uuid}/workspace-boards-archived/`,
        { credentials: "include" }
    );
    return await response.json();
}

export async function getWorkspaceCustomer(
    workspace_uuid: string
): Promise<Customer> {
    const response = await fetch(
        `${vars.API_ENDPOINT}/corporate/workspace/${workspace_uuid}/customer`,
        { credentials: "include" }
    );
    return await response.json();
}
