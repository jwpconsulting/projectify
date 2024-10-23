// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
/**
 * Repository functions for label
 */
import type { Label, WorkspaceDetail } from "$lib/types/workspace";

import { openApiClient } from "../util";

// Create
export async function createLabel(
    { uuid: workspace_uuid }: WorkspaceDetail,
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
