import type { ApolloQueryResult } from "@apollo/client/core";

import { client } from "$lib/graphql/client";
import {
    Mutation_AddWorkspaceBoard,
    Mutation_ArchiveWorkspaceBoard,
    Mutation_UpdateWorkspaceBoard,
} from "$lib/graphql/operations";
import { getWithCredentialsJson, handle404 } from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type {
    Workspace,
    WorkspaceBoard,
} from "$lib/types/workspace";
// WorkspaceBoard CRUD
// Create
export async function createWorkspaceBoard(
    workspace: Workspace,
    workspaceBoard: { title: string; description: string; deadline: null }
): Promise<WorkspaceBoard> {
    const input = {
        workspaceUuid: workspace.uuid,
        ...workspaceBoard,
    };
    const {
        data: { addWorkspaceBoard: createdWorkspaceBoard },
    } = (await client.mutate({
        mutation: Mutation_AddWorkspaceBoard,
        variables: {
            input,
        },
    })) as ApolloQueryResult<{ addWorkspaceBoard: WorkspaceBoard }>;
    return createdWorkspaceBoard;
}

// Read
export async function getWorkspaceBoard(
    uuid: string,
    repositoryContext: RepositoryContext
): Promise<WorkspaceBoard | undefined> {
    return handle404(
        await getWithCredentialsJson<WorkspaceBoard>(
            `/workspace/workspace-board/${uuid}`,
            repositoryContext
        )
    );
}

export async function getArchivedWorkspaceBoards(
    workspace_uuid: string,
    repositoryContext: RepositoryContext
): Promise<undefined | WorkspaceBoard[]> {
    return handle404(
        await getWithCredentialsJson<WorkspaceBoard[]>(
            `/workspace/workspace/${workspace_uuid}/workspace-boards-archived/`,
            repositoryContext
        )
    );
}

// These methods find refuge from SelectWorkspaceBoard.svelte here
export async function updateWorkspaceBoard(workspaceBoard: WorkspaceBoard) {
    await client.mutate({
        mutation: Mutation_UpdateWorkspaceBoard,
        variables: {
            input: {
                uuid: workspaceBoard.uuid,
                title: workspaceBoard.title,
                deadline: workspaceBoard.deadline,
                description: "",
            },
        },
    });
}

export async function archiveWorkspaceBoard(workspaceBoard: WorkspaceBoard) {
    // TODO confirmation dialog
    await client.mutate({
        mutation: Mutation_ArchiveWorkspaceBoard,
        variables: {
            input: {
                uuid: workspaceBoard.uuid,
                archived: true,
            },
        },
    });

    // TODO here we ought to find out the URL of the workspace this
    // workspace board belongs to
    console.error("TODO");
}
