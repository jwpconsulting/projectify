import { derived } from "svelte/store";
import type { Readable } from "svelte/store";

import { selectedLabels } from "$lib/stores/dashboard/labelFilter";
import { currentWorkspaceBoard } from "$lib/stores/dashboard/workspaceBoard";
import { selectedWorkspaceUser } from "$lib/stores/dashboard/workspaceUserFilter";
import type {
    LabelSelection,
    TasksPerUser,
    WorkspaceUserSelection,
} from "$lib/types/ui";
import type { Label, Task, WorkspaceBoardSection } from "$lib/types/workspace";

interface CurrentFilter {
    labels: LabelSelection;
    workspaceUser: WorkspaceUserSelection;
    workspaceBoardSections: WorkspaceBoardSection[];
}

function filterSectionsTasks(
    currentFilter: CurrentFilter
): WorkspaceBoardSection[] {
    let sections: WorkspaceBoardSection[] =
        currentFilter.workspaceBoardSections;
    if (currentFilter.labels.kind === "noLabel") {
        // TODO filter by no label? Justus 2023-04-04
        // eslint-disable-next-line
    } else if (currentFilter.labels.kind === "allLabels") {
        // TODO what to do here?
        // eslint-disable-next-line
    } else {
        const labelUuids = [...currentFilter.labels.labelUuids.keys()];

        sections = sections.map((section) => {
            const sectionTasks = section.tasks ? section.tasks : [];
            const tasks = sectionTasks.filter((task: Task) => {
                return (
                    task.labels.findIndex((l: Label) =>
                        labelUuids.find((labelUuid) => l.uuid === labelUuid)
                            ? true
                            : false
                    ) >= 0
                );
            });

            return {
                ...section,
                tasks,
            };
        });
    }

    const workspaceUserSelection = currentFilter.workspaceUser;
    if (workspaceUserSelection.kind !== "allWorkspaceUsers") {
        sections = sections.map((section) => {
            const sectionTasks = section.tasks ? section.tasks : [];
            const tasks = sectionTasks.filter((task: Task) => {
                if (workspaceUserSelection.kind === "unassigned") {
                    return !task.assignee;
                } else {
                    return task.assignee
                        ? workspaceUserSelection.workspaceUserUuids.has(
                              task.assignee.uuid
                          )
                        : false;
                }
            });

            return {
                ...section,
                tasks,
            };
        });
    }

    return sections;
}

export const currentWorkspaceBoardSections = derived<
    [
        typeof selectedLabels,
        typeof selectedWorkspaceUser,
        typeof currentWorkspaceBoard,
    ],
    WorkspaceBoardSection[] | undefined
>(
    [selectedLabels, selectedWorkspaceUser, currentWorkspaceBoard],
    (
        [$selectedLabels, $selectedWorkspaceUser, $currentWorkspaceBoard],
        set
    ) => {
        if (!$currentWorkspaceBoard) {
            set(undefined);
            return;
        }
        const workspaceBoardSections =
            $currentWorkspaceBoard.workspace_board_sections;
        set(
            filterSectionsTasks({
                labels: $selectedLabels,
                workspaceUser: $selectedWorkspaceUser,
                workspaceBoardSections,
            })
        );
    },
    undefined
);

export const tasksPerUser: Readable<TasksPerUser> = derived<
    Readable<WorkspaceBoardSection[] | undefined>,
    TasksPerUser
>(
    currentWorkspaceBoardSections,
    ($currentWorkspaceBoardSections, set) => {
        if (!$currentWorkspaceBoardSections) {
            return;
        }
        const assigned = new Map<string, number>();
        let unassigned = 0;
        $currentWorkspaceBoardSections.forEach((section) => {
            if (!section.tasks) {
                return;
            }
            section.tasks.forEach((task) => {
                if (!task.assignee) {
                    unassigned = unassigned + 1;
                    return;
                }
                const uuid = task.assignee.uuid;
                assigned.set(uuid, assigned.get(uuid) ?? 0 + 1);
            });
        });
        set({ unassigned, assigned });
    },
    { unassigned: 0, assigned: new Map<string, number>() }
);
