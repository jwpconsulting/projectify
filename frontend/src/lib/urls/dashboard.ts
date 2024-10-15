// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
/**
 * Dashboard urls
 */
import type { ProjectDetail } from "$lib/types/workspace";

export const dashboardUrl = "/dashboard";

export function getProjectSearchUrl({
    uuid,
}: Pick<ProjectDetail, "uuid">): string {
    return `/dashboard/project/${uuid}/search`;
}
