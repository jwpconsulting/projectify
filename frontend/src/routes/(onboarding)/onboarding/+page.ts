// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { redirect } from "@sveltejs/kit";

import { startUrl } from "$lib/urls/onboarding";

export function load() {
    const redirectUrl = startUrl;
    redirect(302, redirectUrl);
}
