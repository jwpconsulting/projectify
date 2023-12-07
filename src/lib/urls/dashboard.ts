/*
 * Dashboard urls
 */

import type { WorkspaceBoard } from "$lib/types/workspace";

export function getWorkspaceBoardSearchUrl(
    { uuid }: Pick<WorkspaceBoard, "uuid">,
    search: string
): string {
    return `/dashboard/workspace-board/${uuid}/search?${encodeURIComponent(
        search
    )}`;
}
