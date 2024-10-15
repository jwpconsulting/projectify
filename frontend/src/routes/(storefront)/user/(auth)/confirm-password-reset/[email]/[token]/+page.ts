// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import type { PageLoadEvent } from "./$types";

interface Data {
    email: string;
    token: string;
}
export function load({ params: { email, token } }: PageLoadEvent): Data {
    return { email, token };
}
