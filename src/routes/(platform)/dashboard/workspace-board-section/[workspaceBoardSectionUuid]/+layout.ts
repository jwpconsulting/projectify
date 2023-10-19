import { getWorkspaceBoardSection } from "$lib/repository/workspace";
import { currentWorkspace } from "$lib/stores/dashboard";
import type { WorkspaceBoardSection } from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

import type { LayoutLoadEvent } from "./$types";

interface Data {
    workspaceBoardSection: WorkspaceBoardSection;
}

export async function load({
    params: { workspaceBoardSectionUuid },
    fetch,
}: LayoutLoadEvent): Promise<Data> {
    // If thing is fetched, use the fetch argument above
    const workspaceBoardSection = await getWorkspaceBoardSection(
        workspaceBoardSectionUuid,
        { fetch }
    );
    const workspaceBoard = unwrap(
        workspaceBoardSection.workspace_board,
        "Expected workspace_board"
    );
    const { uuid: workspaceUuid } = unwrap(
        workspaceBoard.workspace,
        "Expected workspace"
    );
    currentWorkspace.loadUuid(workspaceUuid, { fetch }).catch((reason) => {
        console.error(
            "Tried to load currentWorkspace in background, but failed with",
            reason
        );
    });
    return { workspaceBoardSection };
}
