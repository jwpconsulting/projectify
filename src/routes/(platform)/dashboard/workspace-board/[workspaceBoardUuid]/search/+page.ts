// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
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
        search,
    );
    return { tasks, search };
}
