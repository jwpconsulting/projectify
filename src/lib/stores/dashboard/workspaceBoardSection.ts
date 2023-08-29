import { derived } from "svelte/store";
import type { Readable } from "svelte/store";

import { selectedLabels } from "$lib/stores/dashboard/label";
import { currentWorkspaceBoard } from "$lib/stores/dashboard/workspaceBoard";
import { selectedWorkspaceUser } from "$lib/stores/dashboard/workspaceUser";
import type {
    LabelSelection,
    TasksPerUser,
    WorkspaceUserSelection,
} from "$lib/types/ui";
import type {
    WorkspaceBoard,
    Label,
    Task,
    WorkspaceBoardSection,
} from "$lib/types/workspace";

interface CurrentFilter {
    labels: LabelSelection;
    workspaceUser: WorkspaceUserSelection;
    workspaceBoardSections: WorkspaceBoardSection[];
}

type CurrentWorkspaceBoardSections = Readable<WorkspaceBoardSection[]>;

function createCurrentWorkspaceBoardSections(
    selectedLabels: Readable<LabelSelection>,
    selectedWorkspaceUser: Readable<WorkspaceUserSelection>,
    // TODO here we should make sure that WorkspaceBoard can not be null
    currentWorkspaceBoard: Readable<WorkspaceBoard | null>
): CurrentWorkspaceBoardSections {
    return derived<
        [
            typeof selectedLabels,
            typeof selectedWorkspaceUser,
            typeof currentWorkspaceBoard
        ],
        WorkspaceBoardSection[]
    >(
        [selectedLabels, selectedWorkspaceUser, currentWorkspaceBoard],
        (
            [$selectedLabels, $selectedWorkspaceUser, $currentWorkspaceBoard],
            set
        ) => {
            if (!$currentWorkspaceBoard) {
                return;
            }
            const workspaceBoardSections =
                $currentWorkspaceBoard.workspace_board_sections;
            if (!workspaceBoardSections) {
                return;
            }
            set(
                filterSectionsTasks({
                    labels: $selectedLabels,
                    workspaceUser: $selectedWorkspaceUser,
                    workspaceBoardSections,
                })
            );
        },
        []
    );
}

export const currentWorkspaceBoardSections =
    createCurrentWorkspaceBoardSections(
        selectedLabels,
        selectedWorkspaceUser,
        currentWorkspaceBoard
    );

type CurrentTasksPerUser = Readable<TasksPerUser>;

export function createTasksPerUser(
    currentWorkspaceBoardSections: CurrentWorkspaceBoardSections
): CurrentTasksPerUser {
    return derived<[typeof currentWorkspaceBoardSections], TasksPerUser>(
        [currentWorkspaceBoardSections],
        ([$currentWorkspaceBoardSections], set) => {
            const userCounts = new Map<string, number>();
            let unassignedCounts = 0;
            $currentWorkspaceBoardSections.forEach((section) => {
                if (!section.tasks) {
                    return;
                }
                section.tasks.forEach((task) => {
                    if (task.assignee) {
                        const uuid = task.assignee.uuid;
                        const count = userCounts.get(uuid);
                        if (count) {
                            userCounts.set(uuid, count + 1);
                        } else {
                            userCounts.set(uuid, 1);
                        }
                    } else {
                        unassignedCounts = unassignedCounts + 1;
                    }
                });
            });
            const counts: TasksPerUser = {
                unassigned: unassignedCounts,
                assigned: userCounts,
            };
            set(counts);
        },
        { unassigned: 0, assigned: new Map<string, number>() }
    );
}

export function filterSectionsTasks(
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
