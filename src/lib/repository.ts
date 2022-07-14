import vars from "$lib/env";
import type {
    User,
    WorkspaceBoard,
    Workspace,
    Customer,
    Task,
} from "$lib/types";

async function getWithCredentialsJson<T>(url: string): Promise<T> {
    const response = await fetch(`${vars.API_ENDPOINT}${url}`, {
        credentials: "include",
    });
    const body = await response.json();
    if (!response.ok) {
        throw new Error(`${response.statusText}: ${JSON.stringify(body)}`);
    }
    return body;
}

export async function getUser(): Promise<User | null> {
    try {
        return await getWithCredentialsJson<User>(`/user/user`);
    } catch {
        return null;
    }
}

export async function getWorkspaceBoard(
    uuid: string
): Promise<WorkspaceBoard> {
    return await getWithCredentialsJson<WorkspaceBoard>(
        `/workspace/workspace-board/${uuid}`
    );
}

export async function getWorkspaces(): Promise<Workspace[]> {
    return await getWithCredentialsJson<Workspace[]>(
        `/workspace/user/workspaces/`
    );
}

export async function getWorkspace(uuid: string): Promise<Workspace> {
    return await getWithCredentialsJson<Workspace>(
        `/workspace/workspace/${uuid}`
    );
}

export async function getTask(uuid: string): Promise<Task> {
    return await getWithCredentialsJson<Task>(`/workspace/task/${uuid}`);
}

export async function getArchivedWorkspaceBoards(
    workspace_uuid: string
): Promise<WorkspaceBoard[]> {
    return await getWithCredentialsJson<WorkspaceBoard[]>(
        `/workspace/workspace/${workspace_uuid}/workspace-boards-archived/`
    );
}

export async function getWorkspaceCustomer(
    workspace_uuid: string
): Promise<Customer> {
    return await getWithCredentialsJson<Customer>(
        `/corporate/workspace/${workspace_uuid}/customer`
    );
}
