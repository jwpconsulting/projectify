import type { ApolloQueryResult } from "@apollo/client";

import { client } from "$lib/graphql/client";
import { Mutation_UpdateWorkspace } from "$lib/graphql/operations";
import {
    getWithCredentialsJson,
    postWithCredentialsJson,
} from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type { Workspace } from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

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
//
export async function updateWorkspace(
    uuid: string,
    title: string,
    description?: string
): Promise<Workspace> {
    const result = (await client.mutate({
        mutation: Mutation_UpdateWorkspace,
        variables: {
            input: {
                uuid,
                title,
                description,
            },
        },
    })) as ApolloQueryResult<{ updateWorkspace: Workspace }>;
    return unwrap(
        result.data.updateWorkspace,
        "Expected updateWorkspace"
    ) as Workspace;
}
// Delete
