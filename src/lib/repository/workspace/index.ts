import type { ApolloQueryResult, FetchResult } from "@apollo/client/core";

import { client } from "$lib/graphql/client";
import {
    Mutation_MoveWorkspaceBoardSection,
    Mutation_AddLabelMutation,
    Mutation_AddWorkspaceBoardSection,
    Mutation_DeleteLabelMutation,
} from "$lib/graphql/operations";
import { getWithCredentialsJson, handle404 } from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type {
    CreateWorkspaceBoardSection,
    Label,
    Workspace,
    WorkspaceBoard,
    WorkspaceBoardSection,
} from "$lib/types/workspace";

export * from "$lib/repository/workspace/workspace";
export * from "$lib/repository/workspace/task";

// Label CRUD
export async function createLabel(
    workspace: Workspace,
    name: string,
    color: number
): Promise<Label> {
    const {
        data: { addLabel: label },
    } = (await client.mutate({
        mutation: Mutation_AddLabelMutation,
        variables: {
            input: {
                workspaceUuid: workspace.uuid,
                name,
                color,
            },
        },
    })) as ApolloQueryResult<{ addLabel: Label }>;
    return label;
}

export async function deleteLabel(label: Label) {
    await client.mutate({
        mutation: Mutation_DeleteLabelMutation,
        variables: {
            input: {
                uuid: label.uuid,
            },
        },
    });
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
