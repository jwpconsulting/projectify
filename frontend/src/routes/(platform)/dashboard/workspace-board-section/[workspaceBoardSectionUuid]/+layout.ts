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
import { error } from "@sveltejs/kit";

import { getWorkspaceBoardSection } from "$lib/repository/workspace/workspaceBoardSection";
import { currentWorkspace } from "$lib/stores/dashboard";
import type { WorkspaceBoardSectionDetail } from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

import type { LayoutLoadEvent } from "./$types";

interface Data {
    workspaceBoardSection: WorkspaceBoardSectionDetail;
}

export async function load({
    params: { workspaceBoardSectionUuid },
    fetch,
}: LayoutLoadEvent): Promise<Data> {
    // If thing is fetched, use the fetch argument above
    const workspaceBoardSection = await getWorkspaceBoardSection(
        workspaceBoardSectionUuid,
        { fetch },
    );
    if (!workspaceBoardSection) {
        throw error(
            404,
            `The workspace board section with UUID '${workspaceBoardSectionUuid}' could not be found`,
        );
    }
    const workspaceBoard = workspaceBoardSection.workspace_board;
    const { uuid: workspaceUuid } = unwrap(
        workspaceBoard.workspace,
        "Expected workspace",
    );
    currentWorkspace.loadUuid(workspaceUuid, { fetch }).catch((reason) => {
        console.error(
            "Tried to load currentWorkspace in background, but failed with",
            reason,
        );
    });
    return { workspaceBoardSection };
}
