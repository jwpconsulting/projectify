// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
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
    repositoryContext: RepositoryContext,
): Promise<Result<undefined, DeleteError>> {
    const result = await deleteWithCredentialsJson(
        `/workspace/workspace-user/${workspaceUser.uuid}`,
        repositoryContext,
    );
    if (result.kind === "ok") {
        return { ok: true, result: undefined };
    } else if (result.kind === "badRequest") {
        return { ok: false, error: result.error as DeleteError };
    }
    console.error(result);
    throw new Error("Unrecoverable");
}
