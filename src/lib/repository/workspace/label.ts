/*
 * Repository functions for label
 */

import { client } from "$lib/graphql/client";
import { Mutation_DeleteLabelMutation } from "$lib/graphql/operations";
import type { RepositoryContext } from "$lib/types/repository";
import type { Label, Workspace } from "$lib/types/workspace";

import { postWithCredentialsJson } from "../util";

export async function createLabel(
    workspace: Workspace,
    { name, color }: Pick<Label, "name" | "color">,
    repositoryContext: RepositoryContext
): Promise<Label> {
    const response = await postWithCredentialsJson<Label>(
        `/workspace/label/`,
        { workspace_uuid: workspace.uuid, name, color },
        repositoryContext
    );
    if (response.kind !== "ok") {
        console.error("TODO handle", response);
        throw new Error("Error while creating label");
    }
    return response.data;
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
