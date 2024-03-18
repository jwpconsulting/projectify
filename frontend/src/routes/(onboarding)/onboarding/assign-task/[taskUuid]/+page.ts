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
import { error } from "@sveltejs/kit";

import { getProject } from "$lib/repository/workspace/project";
import { currentTask } from "$lib/stores/dashboard";
import type {
    Label,
    Task,
    Workspace,
    ProjectDetail,
    Section,
    TeamMember,
} from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

import type { PageLoadEvent } from "./$types";

interface returnType {
    task: Task;
    section: Section;
    project: ProjectDetail;
    workspace: Workspace;
    label: Label;
    assignee: TeamMember;
}
export async function load({
    fetch,
    params: { taskUuid },
}: PageLoadEvent): Promise<returnType> {
    const task = await currentTask.loadUuid(taskUuid, { fetch });
    if (!task) {
        // TODO find out if we can i18n this?
        error(404, `No task could be found for task UUID '${taskUuid}'.`);
    }
    const section = task.section;
    const projectUuid = section.project.uuid;
    const project = await getProject(projectUuid, {
        fetch,
    });
    if (!project) {
        throw new Error("Expected project");
    }
    const { workspace } = project;
    const label = unwrap(task.labels.at(0), "Expected label");
    const assignee = unwrap(task.assignee, "Expected assignee");
    return {
        task,
        assignee,
        section,
        project,
        workspace,
        label,
    };
}
