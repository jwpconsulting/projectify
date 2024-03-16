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
// TODO it seems like we could bundle all these [taskUuid] dependent onboarding
// pages like so:
// onboarding/task/[taskUuid]/new-label/
import { error } from "@sveltejs/kit";

import { getTask } from "$lib/repository/workspace";
import { getProject } from "$lib/repository/workspace/project";
import type {
    TaskWithSection,
    Workspace,
    ProjectDetail,
    Section,
} from "$lib/types/workspace";

import type { PageLoadEvent } from "./$types";

interface returnType {
    task: TaskWithSection;
    section: Section;
    project: ProjectDetail;
    workspace: Workspace;
}

export async function load({
    fetch,
    params: { taskUuid },
}: PageLoadEvent): Promise<returnType> {
    const task = await getTask(taskUuid, { fetch });
    if (!task) {
        error(404, `No task could found for UUID ${taskUuid}.`);
    }
    const { section: section } = task;
    const projectUuid = task.section.project.uuid;
    const project = await getProject(projectUuid, {
        fetch,
    });
    if (!project) {
        throw new Error("Expected project");
    }
    const { workspace } = project;
    return { task, section, project, workspace };
}
