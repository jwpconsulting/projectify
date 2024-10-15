// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK
import { openApiClient } from "$lib/repository/util";

export async function load({
    params: { email, token },
}: {
    params: { email: string; token: string };
}) {
    const result = await openApiClient.POST("/user/user/confirm-email", {
        body: { email, token },
    });
    const error: (typeof result)["error"] = result.error;
    return { error };
}
