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

import { getWorkspaceCustomer } from "$lib/repository/corporate";
import type { Customer } from "$lib/types/corporate";
import type { Workspace } from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";

interface Data {
    customer: Customer;
    workspace: Workspace;
}

export async function load({
    params: { workspaceUuid },
    parent,
    fetch,
}: PageLoadEvent): Promise<Data> {
    const { workspace } = await parent();
    const customer = await getWorkspaceCustomer(workspaceUuid, { fetch });
    if (!customer) {
        // TODO maybe better error message here?
        throw error(404);
    }
    return {
        customer,
        workspace,
    };
}
