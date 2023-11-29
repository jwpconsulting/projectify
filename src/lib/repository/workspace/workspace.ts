import {
    getWithCredentialsJson,
    handle404,
    postWithCredentialsJson,
    putWithCredentialsJson,
} from "$lib/repository/util";
import type { Result } from "$lib/types/base";
import type { RepositoryContext } from "$lib/types/repository";
import type { Workspace, WorkspaceDetail } from "$lib/types/workspace";

// Create
export async function createWorkspace(
    title: string,
    description: string | undefined,
    repositoryContext: RepositoryContext
): Promise<Workspace> {
    const response = await postWithCredentialsJson<Workspace>(
        `/workspace/workspaces/`,
        { title, description },
        repositoryContext
    );
    if (response.kind !== "ok") {
        console.error("TODO handle", response);
        throw new Error("Error while creating workspace");
    }
    return response.data;
}
// Read
export async function getWorkspaces(
    repositoryContext: RepositoryContext
): Promise<Workspace[] | undefined> {
    return handle404(
        await getWithCredentialsJson<Workspace[]>(
            `/workspace/user/workspaces/`,
            repositoryContext
        )
    );
}

export async function getWorkspace(
    uuid: string,
    repositoryContext: RepositoryContext
): Promise<WorkspaceDetail | undefined> {
    return handle404(
        await getWithCredentialsJson<WorkspaceDetail>(
            `/workspace/workspace/${uuid}`,
            repositoryContext
        )
    );
}

// Update
export async function updateWorkspace(
    // TODO take workspace type instead of uuid string
    uuid: string,
    title: string,
    description: string | undefined,
    repositoryContext: RepositoryContext
): Promise<Workspace> {
    const response = await putWithCredentialsJson<Workspace>(
        `/workspace/workspace/${uuid}`,
        { title, description },
        repositoryContext
    );
    if (response.kind !== "ok") {
        console.error("TODO handle", response);
        throw new Error("Error while creating workspace");
    }
    return response.data;
}
// Delete

// RPC
export async function inviteUser(
    workspace: Workspace,
    email: string,
    repositoryContext: RepositoryContext
): Promise<Result<{ email: string }, { email: string }>> {
    const { uuid } = workspace;
    const response = await postWithCredentialsJson<
        { email: string },
        { email: string }
    >(
        `/workspace/workspace/${uuid}/invite-user`,
        { email },
        repositoryContext
    );
    if (response.kind === "ok") {
        return { ok: true, result: response.data };
    } else if (response.kind === "badRequest") {
        return { ok: false, error: response.error };
    }
    throw new Error();
}
