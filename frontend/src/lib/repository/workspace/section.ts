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
 * Repository functions for sections
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
    Section,
    SectionDetail,
} from "$lib/types/workspace";

import type { ApiResponse } from "../types";

// Create
export async function createSection(
    { uuid: project_uuid }: WorkspaceBoard,
    { title, description }: Pick<Section, "title" | "description">,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<Section, unknown>> {
    return await postWithCredentialsJson(
        `/workspace/section/`,
        { project_uuid, title, description },
        repositoryContext,
    );
}

// Read
export async function getSection(
    uuid: string,
    repositoryContext: RepositoryContext,
): Promise<SectionDetail | undefined> {
    return handle404(
        await getWithCredentialsJson(
            `/workspace/section/${uuid}`,
            repositoryContext,
        ),
    );
}

// Update
export async function updateSection(
    section: Pick<Section, "uuid" | "title" | "description">,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<void, unknown>> {
    return await putWithCredentialsJson(
        `/workspace/section/${section.uuid}`,
        section,
        repositoryContext,
    );
}

// Delete
export async function deleteSection(
    { uuid }: Pick<Section, "uuid">,
    repositoryContext: RepositoryContext,
): Promise<void> {
    return failOrOk(
        await deleteWithCredentialsJson(
            `/workspace/section/${uuid}`,
            repositoryContext,
        ),
    );
}

// RPC
export async function moveSection(
    { uuid }: Section,
    order: number,
    repositoryContext: RepositoryContext,
) {
    return failOrOk(
        await postWithCredentialsJson(
            `/workspace/section/${uuid}/move`,
            { order },
            repositoryContext,
        ),
    );
}
