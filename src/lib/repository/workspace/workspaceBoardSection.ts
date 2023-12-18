/*
 * Repository functions for workspace board sections
 */
import {
    deleteWithCredentialsJson,
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
    WorkspaceBoardSectionDetail,
} from "$lib/types/workspace";

// Create
export async function createWorkspaceBoardSection(
    { uuid: workspace_board_uuid }: WorkspaceBoard,
    {
        title,
        description,
    }: Pick<WorkspaceBoardSection, "title" | "description">,
    repositoryContext: RepositoryContext,
): Promise<WorkspaceBoardSection> {
    return failOrOk(
        await postWithCredentialsJson(
            `/workspace/workspace-board-section/`,
            { workspace_board_uuid, title, description },
            repositoryContext,
        ),
    );
}

// Read
export async function getWorkspaceBoardSection(
    uuid: string,
    repositoryContext: RepositoryContext,
): Promise<WorkspaceBoardSectionDetail | undefined> {
    return handle404(
        await getWithCredentialsJson(
            `/workspace/workspace-board-section/${uuid}`,
            repositoryContext,
        ),
    );
}

// Update
export async function updateWorkspaceBoardSection(
    workspaceBoardSection: Pick<
        WorkspaceBoardSection,
        "uuid" | "title" | "description"
    >,
    repositoryContext: RepositoryContext,
): Promise<void> {
    return failOrOk(
        await putWithCredentialsJson(
            `/workspace/workspace-board-section/${workspaceBoardSection.uuid}`,
            workspaceBoardSection,
            repositoryContext,
        ),
    );
}

// Delete
export async function deleteWorkspaceBoardSection(
    { uuid }: Pick<WorkspaceBoardSection, "uuid">,
    repositoryContext: RepositoryContext,
): Promise<void> {
    return failOrOk(
        await deleteWithCredentialsJson(
            `/workspace/workspace-board-section/${uuid}`,
            repositoryContext,
        ),
    );
}

// RPC
export async function moveWorkspaceBoardSection(
    { uuid }: WorkspaceBoardSection,
    order: number,
    repositoryContext: RepositoryContext,
) {
    return failOrOk(
        await postWithCredentialsJson(
            `/workspace/workspace-board-section/${uuid}/move`,
            { order },
            repositoryContext,
        ),
    );
}
