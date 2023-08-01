import type { PageLoadEvent } from "./$types";
import { getWorkspaceBoardSection } from "$lib/repository/workspace";
import type { WorkspaceBoardSection } from "$lib/types/workspace";

export async function load({
    params: { workspaceBoardSectionUuid },
    fetch,
}: PageLoadEvent): Promise<{ workspaceBoardSection: WorkspaceBoardSection }> {
    const workspaceBoardSection = await getWorkspaceBoardSection(
        workspaceBoardSectionUuid,
        { fetch }
    );
    return { workspaceBoardSection };
}
