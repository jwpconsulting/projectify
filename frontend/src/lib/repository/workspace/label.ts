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
 * Repository functions for label
 */
import type { Label, Workspace } from "$lib/types/workspace";

import { openApiClient } from "../util";

// Create
export async function createLabel(
    { uuid: workspace_uuid }: Workspace,
    { name, color }: Pick<Label, "name" | "color">,
) {
    return await openApiClient.POST("/workspace/label/", {
        body: { workspace_uuid, name, color },
    });
}

// Read
// Update
// TODO not sure if we can return Label here
export async function updateLabel({ uuid: label_uuid, name, color }: Label) {
    return await openApiClient.PUT("/workspace/label/{label_uuid}", {
        params: { path: { label_uuid } },
        body: { name, color },
    });
}
