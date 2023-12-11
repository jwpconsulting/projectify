import { searchTasks } from "$lib/stores/dashboard";
import type { SearchInput } from "$lib/types/base";
import type { TaskWithWorkspaceBoardSection } from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

import type { PageLoadEvent } from "./$types";

interface Data {
    tasks: TaskWithWorkspaceBoardSection[];
    search: SearchInput;
}

export async function load({ url, parent }: PageLoadEvent): Promise<Data> {
    const { workspaceBoard } = await parent();
    const { workspace_board_sections: workspaceBoardSections } =
        workspaceBoard;
    const search: SearchInput = url.searchParams.get("search") ?? undefined;
    const tasks = searchTasks(
        unwrap(workspaceBoardSections, "Expected workspaceBoardSections"),
        search
    );
    return { tasks, search };
}
