// SPDX-License-Identifier: AGPL-3.0-or-later

import type { components } from "./schema";

// SPDX-FileCopyrightText: 2023 JWP Consulting GK
export type User = components["schemas"]["User"];
export type CurrentUser =
    | components["schemas"]["auth_info"]
    | { kind: "start" };

export function getDisplayName(
    user: Pick<User, "email" | "preferred_name">,
): string {
    if (user.preferred_name) {
        return user.preferred_name;
    }
    return user.email;
}
