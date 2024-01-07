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

import {
    currentWorkspace,
    currentWorkspaceBoard,
    currentWorkspaces,
} from "$lib/stores/dashboard";
import type { Workspace, WorkspaceBoardDetail } from "$lib/types/workspace";

import type { LayoutLoadEvent } from "./$types";

interface Data {
    workspaceBoard: WorkspaceBoardDetail;
    workspace: Workspace;
    workspaces: Workspace[];
}

export async function load({
    params: { workspaceBoardUuid }, // TODO add fetch back and use in subscription somehow
    fetch,
}: LayoutLoadEvent): Promise<Data> {
    const workspaceBoard = await currentWorkspaceBoard.loadUuid(
        workspaceBoardUuid,
        { fetch },
    );
    if (!workspaceBoard) {
        throw error(404);
    }
    const workspaceUuid = workspaceBoard.workspace.uuid;
    if (!workspaceUuid) {
        throw new Error("Expected workspace");
    }
    const workspace = await currentWorkspace.loadUuid(workspaceUuid, {
        fetch,
    });
    if (!workspace) {
        throw error(404);
    }
    // XXX Might be able to do this asynchronously, meaning we don't need to wait
    // for it to finish here?
    const workspaces = await currentWorkspaces.load({ fetch });
    if (!workspaces) {
        throw error(404);
    }
    return { workspace, workspaceBoard, workspaces };
}
