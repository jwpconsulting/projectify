// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { error } from "@sveltejs/kit";

import type { Customer } from "$lib/types/corporate";
import type { WorkspaceDetail } from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";
import { openApiClient } from "$lib/repository/util";

interface Data {
    customer: Customer;
    workspace: WorkspaceDetail;
}

export async function load({
    params: { workspaceUuid },
    parent,
}: PageLoadEvent): Promise<Data> {
    const { workspace } = await parent();
    const { data: customer, error: e } = await openApiClient.GET(
        "/corporate/workspace/{workspace_uuid}/customer",
        { params: { path: { workspace_uuid: workspaceUuid } } },
    );
    if (e !== undefined) {
        error(404);
    }
    return { customer, workspace };
}
