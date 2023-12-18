/*
 * Repository functions for label
 */

import type { RepositoryContext } from "$lib/types/repository";
import type { Label, Workspace } from "$lib/types/workspace";

import {
    deleteWithCredentialsJson,
    failOrOk,
    postWithCredentialsJson,
    putWithCredentialsJson,
} from "../util";

// Create
export async function createLabel(
    workspace: Workspace,
    { name, color }: Pick<Label, "name" | "color">,
    repositoryContext: RepositoryContext,
): Promise<Label> {
    const response = await postWithCredentialsJson<Label>(
        `/workspace/label/`,
        { workspace_uuid: workspace.uuid, name, color },
        repositoryContext,
    );
    if (response.kind !== "ok") {
        console.error("TODO handle", response);
        throw new Error("Error while creating label");
    }
    return response.data;
}

// Read
// Update
// TODO not sure if we can return Label here
export async function updateLabel(
    label: Label,
    repositoryContext: RepositoryContext,
): Promise<void> {
    return failOrOk(
        await putWithCredentialsJson(
            `/workspace/label/${label.uuid}`,
            label,
            repositoryContext,
        ),
    );
}

// Delete
export async function deleteLabel(
    label: Label,
    repositoryContext: RepositoryContext,
) {
    const response = await deleteWithCredentialsJson<Label>(
        `/workspace/label/${label.uuid}`,
        repositoryContext,
    );
    if (response.kind !== "ok") {
        console.error("TODO handle", response);
        throw new Error("Error while creating label");
    }
    return response.data;
}
