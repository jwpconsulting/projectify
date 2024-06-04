// SPDX-License-Identifier: AGPL-3.0-or-later

import type { components } from "./schema";

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
export type User = components["schemas"]["User"];

export function getDisplayName(
    user: Pick<User, "email" | "preferred_name">,
): string {
    if (user.preferred_name) {
        return user.preferred_name;
    }
    return user.email;
}
