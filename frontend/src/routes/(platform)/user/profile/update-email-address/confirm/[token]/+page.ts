// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
/**
 * Page script for email address confirmation
 */
import type { PageLoadEvent } from "./$types";

interface Data {
    token: string;
}

/*
 * Pass token from URL to browser
 */
export function load({ params: { token } }: PageLoadEvent): Data {
    return { token };
}
