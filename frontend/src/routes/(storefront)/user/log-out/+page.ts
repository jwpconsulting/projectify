// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { browser } from "$app/environment";
import { logOut } from "$lib/stores/user";

interface Data {
    result:
        | "not-browser"
        | Promise<{
              error?: { status: "permission_denied"; code: 403 };
              data?: { kind: "unauthenticated" };
          }>;
}

export function load(): Data {
    if (!browser) {
        return { result: "not-browser" };
    }
    return { result: logOut() };
}
