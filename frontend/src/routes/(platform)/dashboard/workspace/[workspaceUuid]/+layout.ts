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

import { clearSelectedWorkspaceUuidIfMatch } from "$lib/stores/dashboard/ui";
import type { WorkspaceDetail } from "$lib/types/workspace";

import type { LayoutLoadEvent } from "./$types";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";

interface Data {
    workspace: WorkspaceDetail;
}

export async function load({
    params: { workspaceUuid },
}: LayoutLoadEvent): Promise<Data> {
    const workspace = await currentWorkspace.loadUuid(workspaceUuid);
    if (!workspace) {
        clearSelectedWorkspaceUuidIfMatch(workspaceUuid);
        error(404, `No workspace found for UUID '${workspaceUuid}'`);
    }
    return { workspace };
}

export const prerender = false;
// TODO Maybe we can set this to true at some point and have SSR support
export const ssr = false;
