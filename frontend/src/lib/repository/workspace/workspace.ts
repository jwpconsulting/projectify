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
import { openApiClient } from "$lib/repository/util";
import type { UserWorkspace } from "$lib/types/workspace";

// Read
export async function getWorkspaces(): Promise<UserWorkspace[]> {
    const { error, data } = await openApiClient.GET(
        "/workspace/workspace/user-workspaces/",
    );
    if (error?.code === 500) {
        console.error("Could not retrieve workspaces, retrying");
        throw new Error();
    }
    if (data) {
        return data;
    }
    throw new Error(`Could not retrieve workspaces ${JSON.stringify(error)}`);
}

export async function getWorkspace(workspace_uuid: string) {
    const { error, data } = await openApiClient.GET(
        "/workspace/workspace/{workspace_uuid}",
        {
            params: { path: { workspace_uuid } },
        },
    );
    if (error?.code === 404) {
        return undefined;
    }
    if (error) {
        throw new Error(
            `Error when retrieving workspace ${workspace_uuid} ${JSON.stringify(
                error,
            )}`,
        );
    }
    return data;
}
