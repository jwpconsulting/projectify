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
import { derived, type Readable } from "svelte/store";

import { getWorkspaceCustomer } from "$lib/repository/corporate";
import { currentWorkspace } from "$lib/stores/dashboard/workspace";
import type { Customer } from "$lib/types/corporate";

type CurrentCustomer = Readable<Customer | undefined>;

export const currentCustomer: CurrentCustomer = derived<
    typeof currentWorkspace,
    Customer | undefined
>(currentWorkspace, ($currentWorkspace, set) => {
    const uuid = $currentWorkspace?.uuid;
    if (!uuid) {
        return;
    }
    // Hopefully this won't be run server-side, fetch is not available
    // there
    getWorkspaceCustomer(uuid, { fetch })
        .then(set)
        .catch((error: Error) => {
            console.error(
                "An error happened when fetching the currentCustomer",
                { error },
            );
        });
});
