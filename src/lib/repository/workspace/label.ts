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
