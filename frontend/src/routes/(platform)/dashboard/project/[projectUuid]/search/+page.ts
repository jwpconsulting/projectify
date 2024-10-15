// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { searchTasks } from "$lib/stores/dashboard/task";
import type { SearchInput } from "$lib/types/base";
import type { TaskWithSection } from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

import type { PageLoadEvent } from "./$types";

interface Data {
    tasks: Promise<readonly TaskWithSection[]>;
    search: SearchInput;
}
export function load({ url, parent }: PageLoadEvent): Data {
    const search: SearchInput = url.searchParams.get("search") ?? undefined;
    const tasks = (async () => {
        const data = await parent();
        const project = await data.project;
        if (project === undefined) {
            throw new Error("Expected project");
        }
        const { sections } = project;
        const tasks = searchTasks(
            unwrap(sections, "Expected sections"),
            search,
        );
        return tasks;
    })();
    return { tasks, search };
}
