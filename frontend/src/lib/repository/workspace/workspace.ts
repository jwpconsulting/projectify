// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023-2024 JWP Consulting GK
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
import {
    openApiClient,
    postWithCredentialsJson,
    putWithCredentialsJson,
} from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type { Workspace, WorkspaceDetail } from "$lib/types/workspace";

import type { ApiResponse } from "../types";

// Create
export async function createWorkspace(
    title: string,
    description: string | undefined,
    repositoryContext: RepositoryContext,
): Promise<Workspace> {
    const response = await postWithCredentialsJson<Workspace>(
        `/workspace/workspace/`,
        { title, description },
        repositoryContext,
    );
    if (response.kind !== "ok") {
        console.error("TODO handle", response);
        throw new Error("Error while creating workspace");
    }
    return response.data;
}
// Read
export async function getWorkspaces(
    _repositoryContext?: RepositoryContext,
): Promise<Workspace[]> {
    const { response, data } = await openApiClient.GET(
        "/workspace/workspace/user-workspaces/",
    );
    if (data !== undefined) {
        return data;
    }
    throw new Error(
        `Could not retrieve workspaces ${JSON.stringify(
            await response.json(),
        )}`,
    );
}

export async function getWorkspace(
    workspace_uuid: string,
    _repositoryContext?: RepositoryContext,
): Promise<WorkspaceDetail | undefined> {
    const { response, data } = await openApiClient.GET(
        "/workspace/workspace/{workspace_uuid}",
        { params: { path: { workspace_uuid } } },
    );
    if (data !== undefined) {
        return data;
    }
    throw new Error(
        `Could not retrieve workspace ${workspace_uuid}, ${JSON.stringify(
            await response.json(),
        )}`,
    );
}

// Update
export async function updateWorkspace(
    // TODO take workspace type instead of uuid string
    uuid: string,
    title: string,
    description: string | null,
    repositoryContext: RepositoryContext,
): Promise<Workspace> {
    const response = await putWithCredentialsJson<Workspace>(
        `/workspace/workspace/${uuid}`,
        { title, description },
        repositoryContext,
    );
    if (response.kind !== "ok") {
        throw new Error("Error while updating workspace");
    }
    return response.data;
}
// Delete

// RPC
export async function inviteUser(
    { uuid }: Pick<Workspace, "uuid">,
    email: string,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<unknown, { email?: string }>> {
    return await postWithCredentialsJson(
        `/workspace/workspace/${uuid}/invite-team-member`,
        { email },
        repositoryContext,
    );
}

export async function uninviteUser(
    { uuid }: Pick<Workspace, "uuid">,
    email: string,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<unknown, { email?: string }>> {
    return await postWithCredentialsJson(
        `/workspace/workspace/${uuid}/uninvite-team-member`,
        { email },
        repositoryContext,
    );
}
