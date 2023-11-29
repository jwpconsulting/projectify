/*
 * Repository functions for label
 */
import type { ApolloQueryResult } from "@apollo/client/core";

import { client } from "$lib/graphql/client";
import {
    Mutation_AddLabelMutation,
    Mutation_DeleteLabelMutation,
} from "$lib/graphql/operations";
import type { Label, Workspace } from "$lib/types/workspace";

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
