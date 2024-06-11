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
import { openApiClient } from "$lib/repository/util";
import type { ProjectDetail } from "$lib/types/workspace";

// Project CRUD
// Read
export async function getProject(
    project_uuid: string,
): Promise<ProjectDetail | undefined> {
    const { error, data } = await openApiClient.GET(
        "/workspace/project/{project_uuid}",
        { params: { path: { project_uuid } } },
    );
    if (error?.code === 500) {
        throw new Error("Unrecoverable server error");
    }
    if (data) {
        return data;
    }
    return undefined;
}
