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
    ArchivedWorkspaceBoard,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardDetail,
} from "$lib/types/workspace";

// WorkspaceBoard CRUD
// Create
export async function createWorkspaceBoard(
    workspace: Workspace,
    workspaceBoard: { title: string; description: string; deadline?: string },
    repositoryContext: RepositoryContext
): Promise<WorkspaceBoard> {
    const { title, description, deadline } = workspaceBoard;
    const { uuid: workspace_uuid } = workspace;
    const response = await postWithCredentialsJson<Workspace>(
        `/workspace/workspace-board/`,
        { workspace_uuid, title, description, deadline },
        repositoryContext
    );
    if (response.kind !== "ok") {
        console.error("TODO handle", response);
        throw new Error("Error while creating workspace  board");
    }
    return response.data;
}

// Read
export async function getWorkspaceBoard(
    uuid: string,
    repositoryContext: RepositoryContext
): Promise<WorkspaceBoardDetail | undefined> {
    return handle404(
        await getWithCredentialsJson<WorkspaceBoardDetail>(
            `/workspace/workspace-board/${uuid}`,
            repositoryContext
        )
    );
}

export async function getArchivedWorkspaceBoards(
    workspace_uuid: string,
    repositoryContext: RepositoryContext
): Promise<undefined | ArchivedWorkspaceBoard[]> {
    return handle404(
        await getWithCredentialsJson<ArchivedWorkspaceBoard[]>(
            `/workspace/workspace/${workspace_uuid}/archived-workspace-boards/`,
            repositoryContext
        )
    );
}

// Update
export async function updateWorkspaceBoard(
    workspaceBoard: Pick<
        WorkspaceBoard,
        "title" | "description" | "uuid" | "deadline"
    >,
    repositoryContext: RepositoryContext
) {
    return failOrOk(
        await putWithCredentialsJson(
            `/workspace/workspace-board/${workspaceBoard.uuid}`,
            workspaceBoard,
            repositoryContext
        )
    );
}
// Delete
export async function deleteWorkspaceBoard(
    { uuid }: WorkspaceBoard,
    repositoryContext: RepositoryContext
): Promise<void> {
    failOrOk(
        await deleteWithCredentialsJson(
            `/workspace/workspace-board/${uuid}`,
            repositoryContext
        )
    );
}

export async function archiveWorkspaceBoard(
    { uuid }: WorkspaceBoard,
    archived: boolean,
    repositoryContext: RepositoryContext
) {
    failOrOk(
        await postWithCredentialsJson(
            `/workspace/workspace-board/${uuid}/archive`,
            { archived },
            repositoryContext
        )
    );
}
