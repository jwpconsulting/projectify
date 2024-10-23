// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { error } from "@sveltejs/kit";

import { getProject } from "$lib/repository/workspace/project";
import { currentTask } from "$lib/stores/dashboard/task";
import type {
    Label,
    ProjectDetailWorkspace,
    ProjectDetail,
    ProjectDetailAssignee,
    TaskDetail,
    ProjectDetailSection,
} from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

import type { PageLoadEvent } from "./$types";

interface returnType {
    task: TaskDetail;
    section: ProjectDetailSection;
    project: ProjectDetail;
    workspace: ProjectDetailWorkspace;
    label: Label;
    assignee: ProjectDetailAssignee;
}
export async function load({
    params: { taskUuid },
}: PageLoadEvent): Promise<returnType> {
    const task = await currentTask.loadUuid(taskUuid);
    if (!task) {
        // TODO find out if we can i18n this?
        error(404, `No task could be found for task UUID '${taskUuid}'.`);
    }
    const {
        section: {
            uuid: sectionUuid,
            project: { uuid: projectUuid },
        },
    } = task;
    const project = await getProject(projectUuid);
    if (!project) {
        throw new Error("Expected project");
    }
    const section = project.sections.find((s) => s.uuid === sectionUuid);
    if (!section) {
        throw new Error("Expected section");
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
