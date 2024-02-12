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
 * Repository functions for workspace board sections
 */
import {
    deleteWithCredentialsJson,
    failOrOk,
    getWithCredentialsJson,
    handle404,
    postWithCredentialsJson,
    putWithCredentialsJson,
} from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type {
    WorkspaceBoard,
    WorkspaceBoardSection,
    WorkspaceBoardSectionDetail,
} from "$lib/types/workspace";

import type { ApiResponse } from "../types";

// Create
export async function createWorkspaceBoardSection(
    { uuid: workspace_board_uuid }: WorkspaceBoard,
    {
        title,
        description,
    }: Pick<WorkspaceBoardSection, "title" | "description">,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<WorkspaceBoardSection, unknown>> {
    return await postWithCredentialsJson(
        `/workspace/workspace-board-section/`,
        { workspace_board_uuid, title, description },
        repositoryContext,
    );
}

// Read
export async function getWorkspaceBoardSection(
    uuid: string,
    repositoryContext: RepositoryContext,
): Promise<WorkspaceBoardSectionDetail | undefined> {
    return handle404(
        await getWithCredentialsJson(
            `/workspace/workspace-board-section/${uuid}`,
            repositoryContext,
        ),
    );
}

// Update
export async function updateWorkspaceBoardSection(
    workspaceBoardSection: Pick<
        WorkspaceBoardSection,
        "uuid" | "title" | "description"
    >,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<void, unknown>> {
    return await putWithCredentialsJson(
        `/workspace/workspace-board-section/${workspaceBoardSection.uuid}`,
        workspaceBoardSection,
        repositoryContext,
    );
}

// Delete
export async function deleteWorkspaceBoardSection(
    { uuid }: Pick<WorkspaceBoardSection, "uuid">,
    repositoryContext: RepositoryContext,
): Promise<void> {
    return failOrOk(
        await deleteWithCredentialsJson(
            `/workspace/workspace-board-section/${uuid}`,
            repositoryContext,
        ),
    );
}

// RPC
export async function moveWorkspaceBoardSection(
    { uuid }: WorkspaceBoardSection,
    order: number,
    repositoryContext: RepositoryContext,
) {
    return failOrOk(
        await postWithCredentialsJson(
            `/workspace/workspace-board-section/${uuid}/move`,
            { order },
            repositoryContext,
        ),
    );
}
