import type { FetchResult } from "@apollo/client/core";

import { client } from "$lib/graphql/client";
import {
    Mutation_MoveWorkspaceBoardSection,
    Mutation_AddWorkspaceBoardSection,
} from "$lib/graphql/operations";
import { getWithCredentialsJson, handle404 } from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type {
    CreateWorkspaceBoardSection,
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
    workspaceBoard: WorkspaceBoard,
    workspaceBoardSection: CreateWorkspaceBoardSection
): Promise<WorkspaceBoardSection> {
    const result: FetchResult<{
        addWorkspaceBoardSection: WorkspaceBoardSection;
    }> = await client.mutate({
        mutation: Mutation_AddWorkspaceBoardSection,
        variables: {
            input: {
                workspaceBoardUuid: workspaceBoard.uuid,
                ...workspaceBoardSection,
            },
        },
    });
    if (!result.data) {
        throw new Error("Expected result.data");
    }
    return result.data.addWorkspaceBoardSection;
}

// Read
// Update
export async function moveWorkspaceBoardSection(
    { uuid }: WorkspaceBoardSection,
    order: number
) {
    await client.mutate({
        mutation: Mutation_MoveWorkspaceBoardSection,
        variables: {
            input: {
                workspaceBoardSectionUuid: uuid,
                order,
            },
        },
    });
}
