// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
export async function goto(url: string) {
    const { goto } = await import("$app/navigation");
    await goto(url);
}
