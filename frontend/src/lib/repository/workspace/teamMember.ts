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
import type { RepositoryContext } from "$lib/types/repository";
import type { TeamMember } from "$lib/types/workspace";

import type { ApiResponse } from "../types";
import { putWithCredentialsJson } from "../util";

// Create
// Read
// Update
export async function updateTeamMember(
    teamMember: Pick<TeamMember, "uuid" | "role" | "job_title">,
    repositoryContext: RepositoryContext,
): Promise<ApiResponse<undefined, { role?: string; job_title?: string }>> {
    return await putWithCredentialsJson(
        `/workspace/team-member/${teamMember.uuid}`,
        teamMember,
        repositoryContext,
    );
}
