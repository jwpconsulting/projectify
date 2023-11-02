import type { Result } from "$lib/types/base";
import type { RepositoryContext } from "$lib/types/repository";
import type { WorkspaceUser } from "$lib/types/workspace";

import { deleteWithCredentialsJson } from "../util";

// Create
// Read
// Update
// Delete
interface DeleteError {
    workspaceUser: string;
}
export async function deleteWorkspaceUser(
    workspaceUser: WorkspaceUser,
    repositoryContext: RepositoryContext
): Promise<Result<undefined, DeleteError>> {
    const result = await deleteWithCredentialsJson(
        `/workspace/workspace-user/${workspaceUser.uuid}`,
        {},
        repositoryContext
    );
    if (result.kind === "ok") {
        return { ok: true, result: undefined };
    } else if (result.kind === "badRequest") {
        return { ok: false, error: result.error as DeleteError };
    }
    console.error(result);
    throw new Error("Unrecoverable");
}
