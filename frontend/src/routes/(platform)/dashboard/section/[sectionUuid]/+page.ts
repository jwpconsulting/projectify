// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { redirect } from "@sveltejs/kit";

import { getDashboardProjectUrl } from "$lib/urls";
import type { PageLoadEvent } from "./$types";

export async function load({ parent }: PageLoadEvent) {
    const { section } = await parent();
    redirect(302, getDashboardProjectUrl(section.project));
}
