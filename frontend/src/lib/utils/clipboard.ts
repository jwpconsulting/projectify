// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
export async function copyToClipboard(value: string) {
    await navigator.clipboard.writeText(value);
}
