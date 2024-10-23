// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
/**
 * Tailwind related helpers
 */

/*
 * Mark a string as a tailwind class string
 */
export function tw(
    strings: TemplateStringsArray,
    ...values: unknown[]
): string {
    return String.raw({ raw: strings }, ...values);
}
