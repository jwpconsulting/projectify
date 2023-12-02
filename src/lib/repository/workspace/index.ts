import {
    failOrOk,
    getWithCredentialsJson,
    handle404,
    postWithCredentialsJson,
} from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type {
    WorkspaceBoard,
    WorkspaceBoardSection,
} from "$lib/types/workspace";

export * from "$lib/repository/workspace/workspace";
export * from "$lib/repository/workspace/task";

// Label CRUD

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

// WorkspaceBoardSection CRUD
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
// Update
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
