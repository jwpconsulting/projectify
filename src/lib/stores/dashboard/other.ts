import { goto } from "$app/navigation";
import { getDashboardWorkspaceBoardUrl } from "$lib/urls";

import { currentWorkspaceBoardUuid } from "$lib/stores/dashboard/workspaceBoard";

export async function setAndNavigateWorkspaceBoard(uuid: string) {
    currentWorkspaceBoardUuid.set(uuid);
    goto(getDashboardWorkspaceBoardUrl(uuid));
}
