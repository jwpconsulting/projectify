/*
 * Repository functions for workspace board sections
 */
import {
    failOrOk,
    getWithCredentialsJson,
    handle404,
    postWithCredentialsJson,
    putWithCredentialsJson,
} from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type {
    WorkspaceBoard,
    WorkspaceBoardSection,
} from "$lib/types/workspace";

// Create
export async function createWorkspaceBoardSection(
    { uuid: workspace_board_uuid }: WorkspaceBoard,
    {
        title,
        description,
    }: Pick<WorkspaceBoardSection, "title" | "description">,
    repositoryContext: RepositoryContext
): Promise<WorkspaceBoardSection> {
    return failOrOk(
        await postWithCredentialsJson(
            `/workspace/workspace-board-section/`,
            { workspace_board_uuid, title, description },
            repositoryContext
        )
    );
}

// Read
export async function getWorkspaceBoardSection(
    uuid: string,
    repositoryContext: RepositoryContext
): Promise<WorkspaceBoardSection | undefined> {
    return handle404(
        await getWithCredentialsJson<WorkspaceBoardSection>(
            `/workspace/workspace-board-section/${uuid}`,
            repositoryContext
        )
    );
}

// Update
export async function updateWorkspaceBoardSection(
    workspaceBoardSection: Pick<
        WorkspaceBoardSection,
        "uuid" | "title" | "description"
    >,
    repositoryContext: RepositoryContext
): Promise<void> {
    return failOrOk(
        await putWithCredentialsJson(
            `/workspace/workspace-board-section/${workspaceBoardSection.uuid}`,
            workspaceBoardSection,
            repositoryContext
        )
    );
}

// Delete
// RPC
export async function moveWorkspaceBoardSection(
    { uuid }: WorkspaceBoardSection,
    order: number,
    repositoryContext: RepositoryContext
) {
    return failOrOk(
        await postWithCredentialsJson(
            `/workspace/workspace-board-section/${uuid}/move`,
            { order },
            repositoryContext
        )
    );
}
