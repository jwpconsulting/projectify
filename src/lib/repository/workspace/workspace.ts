import {
    getWithCredentialsJson,
    postWithCredentialsJson,
} from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type { Workspace } from "$lib/types/workspace";

// Create
export async function createWorkspace(
    title: string,
    description?: string,
    repositoryContext?: RepositoryContext
): Promise<Workspace> {
    return await postWithCredentialsJson<Workspace>(
        `/workspace/workspaces/`,
        { title, description },
        repositoryContext
    );
}
// Read
export async function getWorkspaces(
    repositoryContext?: RepositoryContext
): Promise<Workspace[]> {
    return await getWithCredentialsJson<Workspace[]>(
        `/workspace/user/workspaces/`,
        repositoryContext
    );
}

export async function getWorkspace(
    uuid: string,
    repositoryContext?: RepositoryContext
): Promise<Workspace> {
    return await getWithCredentialsJson<Workspace>(
        `/workspace/workspace/${uuid}`,
        repositoryContext
    );
}

// Update
// Delete
