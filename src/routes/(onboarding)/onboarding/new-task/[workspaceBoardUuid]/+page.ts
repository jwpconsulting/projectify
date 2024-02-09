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

import { getWorkspace } from "$lib/repository/workspace";
import { getWorkspaceBoard } from "$lib/repository/workspace/workspaceBoard";
import type {
    WorkspaceBoardDetail,
    WorkspaceBoardSection,
    WorkspaceDetail,
} from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";

export async function load({
    params: { workspaceBoardUuid },
    fetch,
}: PageLoadEvent): Promise<{
    workspaceBoard: WorkspaceBoardDetail;
    workspace: WorkspaceDetail;
    workspaceBoardSection?: WorkspaceBoardSection;
}> {
    const workspaceBoard = await getWorkspaceBoard(workspaceBoardUuid, {
        fetch,
    });
    if (!workspaceBoard) {
        throw error(
            404,
            `No workspace board could be found for UUID ${workspaceBoardUuid}.`,
        );
    }
    const { uuid: workspaceUuid } = workspaceBoard.workspace;
    const workspace = await getWorkspace(workspaceUuid, {
        fetch,
    });
    if (!workspace) {
        // If this happens something is very wrong
        throw error(
            500,
            `No workspace with UUID ${workspaceUuid} could be found for workspace board UUID ${workspaceBoardUuid}.`,
        );
    }
    const workspaceBoardSection =
        workspaceBoard.workspace_board_sections.at(0);
    return { workspaceBoard, workspace, workspaceBoardSection };
}
