import type { ApolloQueryResult } from "@apollo/client";

import { client } from "$lib/graphql/client";
import { Mutation_UpdateWorkspace } from "$lib/graphql/operations";
import {
    getWithCredentialsJson,
    handle404,
    postWithCredentialsJson,
} from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type { Workspace } from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

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
): Promise<Workspace | undefined> {
    return handle404(
        await getWithCredentialsJson<Workspace>(
            `/workspace/workspace/${uuid}`,
            repositoryContext
        )
    );
}

// Update
// TODO please make me a normal DRF API call
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

// RPC
export async function inviteUser(
    workspace: Workspace,
    email: string,
    repositoryContext: RepositoryContext
): Promise<{ email: string }> {
    const { uuid } = workspace;
    const response = await postWithCredentialsJson<{ email: string }>(
        `/workspace/workspace/${uuid}/invite-user`,
        { email },
        repositoryContext
    );
    if (response.kind === "ok") {
        return response.data;
    } else if (response.kind === "badRequest") {
        // TODO here we shall do something with the error
        const { error } = response;
        console.error(error);
    }
    throw new Error();
}
