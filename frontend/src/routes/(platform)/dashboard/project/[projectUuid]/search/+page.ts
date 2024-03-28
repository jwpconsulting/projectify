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
import type { ProjectDetail, TaskWithSection } from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

import type { PageLoadEvent } from "./$types";

interface Data {
    tasks: Promise<TaskWithSection[]>;
    search: SearchInput;
}
export function load({ url, parent }: PageLoadEvent): Data {
    const search: SearchInput = url.searchParams.get("search") ?? undefined;
    const awaitProject = new Promise<ProjectDetail | undefined>((resolve) =>
        parent().then(({ project }) => resolve(project)),
    );
    const tasks = awaitProject.then((project) => {
        if (project === undefined) {
            throw new Error("Expected project");
        }
        const { sections: sections } = project;
        const tasks = searchTasks(
            unwrap(sections, "Expected sections"),
            search,
        );
        return tasks;
    });
    return { tasks, search };
}
