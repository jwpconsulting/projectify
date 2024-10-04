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
import { derived, readonly, writable } from "svelte/store";
import { persisted } from "svelte-local-storage-store";

import { page } from "$app/stores";
import { currentProject } from "./project";
import type {
    ProjectDetail,
    ProjectDetailSection,
    ProjectDetailTask,
} from "$lib/types/workspace";

/*
 * Store which workspace we have seen last.
 * When we fetch a workspace based on this uuid, we must invalidate it
 * on a 404 workspace not found
 */
const _selectedWorkspaceUuid = persisted<string | null>(
    "selected-workspace-uuid",
    null,
);
export const selectedWorkspaceUuid = readonly(_selectedWorkspaceUuid);
export function selectWorkspaceUuid(uuid: string) {
    _selectedWorkspaceUuid.set(uuid);
}
/*
 * Clear a selected workspace uuid, if it matches the uuid arg
 */
export function clearSelectedWorkspaceUuidIfMatch(uuid: string) {
    _selectedWorkspaceUuid.update(($uuid) => {
        if ($uuid === uuid) {
            return null;
        }
        return $uuid;
    });
}

const _selectedProjectUuids = persisted<Map<string, string>>(
    "selected-project-uuid",
    new Map(),
    {
        serializer: {
            // XXX Using json.parse, maybe a security problem?
            parse(value: string): Map<string, string> {
                const values = JSON.parse(value) as [string, string][];
                try {
                    return new Map(values);
                } catch {
                    return new Map();
                }
            },
            stringify(map: Map<string, string>): string {
                const values: [string, string][] = Array.from(map);
                return JSON.stringify(values);
            },
        },
    },
);
export const selectedProjectUuids = readonly(_selectedProjectUuids);
export function selectProjectUuid(workspaceUuid: string, projectUuid: string) {
    _selectedProjectUuids.update(($selectedProjectUuids) => {
        $selectedProjectUuids.set(workspaceUuid, projectUuid);
        return $selectedProjectUuids;
    });
}

const _projectExpandOpen = persisted("board-expand-open", true);
export const projectExpandOpen = readonly(_projectExpandOpen);
export function toggleProjectExpandOpen() {
    _projectExpandOpen.update((state) => !state);
}

const _userExpandOpen = persisted("user-expand-open", true);
export const userExpandOpen = readonly(_userExpandOpen);
export function toggleUserExpandOpen() {
    _userExpandOpen.update((state) => !state);
}

const _labelExpandOpen = persisted("label-expand-open", true);
export const labelExpandOpen = readonly(_labelExpandOpen);
// TODO rename toggleLabelExpandOpen
export function toggleLabelDropdownClosedNavOpen() {
    _labelExpandOpen.update((state) => !state);
}

const _sideNavOpen = persisted("side-nav-open", true);
export const sideNavOpen = readonly(_sideNavOpen);
export function toggleSideNavOpen() {
    _sideNavOpen.update((state) => !state);
}

const _sectionClosed = persisted("section-closed", new Set<string>(), {
    serializer: {
        // XXX Using json.parse, maybe a security problem?
        parse(value: string): Set<string> {
            const values = JSON.parse(value) as string[];
            try {
                return new Set(values);
            } catch {
                return new Set();
            }
        },
        stringify(set: Set<string>): string {
            const values: string[] = [...set];
            return JSON.stringify(values);
        },
    },
});
export const sectionClosed = readonly(_sectionClosed);

export function toggleSectionOpen(sectionUuid: string) {
    _sectionClosed.update(($sectionClosed) => {
        if ($sectionClosed.has(sectionUuid)) {
            $sectionClosed.delete(sectionUuid);
        } else {
            $sectionClosed.add(sectionUuid);
        }
        return $sectionClosed;
    });
}

// Adjust this if the dashboard URLs ever change
const showFilterRouteIds = ["/(platform)/dashboard/project/[projectUuid]"];

/*
 * showFilters is true only for pages for which we show the user
 * the filter user / label options
 */
export const showFilters = derived<typeof page, boolean>(
    page,
    ($page, set) => {
        const { route } = $page;
        const { id } = route;
        set(showFilterRouteIds.find((i) => i === id) !== undefined);
    },
    false,
);

type SectionTaskSelection =
    | {
          kind: "task-selected";
          project: ProjectDetail;
          sectionUuid: string;
          taskUuid: string;
      }
    | {
          kind: "section-selected";
          project: ProjectDetail;
          sectionUuid: string;
          taskUuid: undefined;
      }
    | {
          kind: "project-selected";
          project: ProjectDetail;
          sectionUuid: undefined;
          taskUuid: undefined;
      }
    | undefined;

const _currentSectionTask = writable<SectionTaskSelection>(
    undefined,
    (set, update) => {
        const unsubscriber = currentProject.subscribe(($currentProject) => {
            const project = $currentProject.value;
            const projectUuid = project?.uuid;
            if (!projectUuid) {
                set(undefined);
            } else {
                update(($currentSectionTask) => {
                    // if no current selection, overwrite
                    if ($currentSectionTask?.project.uuid === projectUuid) {
                        return;
                    } else {
                        return {
                            kind: "project-selected",
                            project,
                            sectionUuid: undefined,
                            taskUuid: undefined,
                        };
                    }
                });
            }
        });
        return unsubscriber;
    },
);

export const currentSectionTask = readonly(_currentSectionTask);

// XXX this is very complicated code, but it works
// Possible scenarios
// current   input        action
// project   next section select 1st section (if exist), 1st task (if exist)
// project   next task    select 1st section (if exist), 1st task (if exist)
// project   prev section select 1st section (if exist), 1st task (if exist)
// project   prev task    select 1st section (if exist), 1st task (if exist)
// section   next section select next section (if exist), 1st task (if exist)
// section   next task    select 1st task (if exist)
// section   prev section select prev section (if exist), 1st task (if exist)
// section   prev task    select prev section (if exist), 1st task (if exist)
// task      next section select next section, 1st task (if exist)
// task      next task    select next task across sections (if exist)
// task      prev section select prev section, last task (if exist)
// task      prev task    select prev task across sections (if exist)
// undefined next section select 1st section (if exist), 1st task (if exist)
// undefined next task    select 1st section (if exist), 1st task (if exist)
// undefined prev section select 1st section (if exist), 1st task (if exist)
// undefined prev task    select 1st section (if exist), 1st task (if exist)
type SelectionKind =
    | "prev-section"
    | "prev-task"
    | "next-section"
    | "next-task";
export function selectInProject(
    project: ProjectDetail | undefined,
    action: SelectionKind,
) {
    if (project === undefined) {
        _currentSectionTask.set(undefined);
        return;
    }
    _currentSectionTask.update(
        ($currentSectionTask: SectionTaskSelection): SectionTaskSelection => {
            if (
                $currentSectionTask === undefined ||
                $currentSectionTask.kind === "project-selected"
            ) {
                const firstSection = project.sections.at(0);
                const firstTask = firstSection?.tasks.at(0);
                if (firstSection !== undefined && firstTask !== undefined) {
                    return {
                        kind: "task-selected",
                        taskUuid: firstTask.uuid,
                        sectionUuid: firstSection.uuid,
                        project,
                    };
                }
                throw new Error("fall-through");
            }

            const sectionIx = project.sections.findIndex(
                (s: ProjectDetailSection) =>
                    s.uuid === $currentSectionTask.sectionUuid,
            );
            const section = project.sections[sectionIx];
            if (!section) {
                throw new Error("Expected section");
            }
            const nextSectionIx = sectionIx + 1;
            const nextSection = project.sections[nextSectionIx];
            const nextSectionTask = nextSection?.tasks[0];
            const prevSectionIx = sectionIx - 1;
            const prevSection = project.sections[prevSectionIx];
            const prevSectionTask = prevSection?.tasks[0];

            const taskIx = section.tasks.findIndex(
                (t: ProjectDetailTask) =>
                    t.uuid === $currentSectionTask.taskUuid,
            );
            const task = section.tasks[taskIx];
            const prevTask = section.tasks[taskIx - 1];
            const nextTask = section.tasks[taskIx + 1];
            const lastTask = prevSection?.tasks.at(-1);
            const firstTask = nextSection?.tasks[0];
            if ($currentSectionTask.kind === "section-selected") {
                switch (action) {
                    case "next-section": {
                        if (nextSection && nextSectionTask) {
                            return {
                                ...$currentSectionTask,
                                kind: "task-selected",
                                sectionUuid: nextSection.uuid,
                                taskUuid: nextSectionTask.uuid,
                            };
                        } else if (nextSection) {
                            return {
                                ...$currentSectionTask,
                                sectionUuid: nextSection.uuid,
                            };
                        } else {
                            return $currentSectionTask;
                        }
                    }
                    case "next-task": {
                        const taskUuid = section.tasks[0]?.uuid;
                        if (taskUuid) {
                            return {
                                ...$currentSectionTask,
                                kind: "task-selected",
                                taskUuid,
                            };
                        } else {
                            return $currentSectionTask;
                        }
                    }
                    case "prev-task":
                    case "prev-section": {
                        if (prevSection && prevSectionTask) {
                            return {
                                ...$currentSectionTask,
                                kind: "task-selected",
                                sectionUuid: prevSection.uuid,
                                taskUuid: prevSectionTask.uuid,
                            };
                        } else if (prevSection) {
                            return {
                                ...$currentSectionTask,
                                sectionUuid: prevSection.uuid,
                            };
                        } else {
                            return $currentSectionTask;
                        }
                    }
                }
            } else {
                if (!task) {
                    throw new Error("Expected task");
                }
                switch (action) {
                    case "next-section": {
                        if (nextSection && nextSectionTask) {
                            return {
                                ...$currentSectionTask,
                                kind: "task-selected",
                                sectionUuid: nextSection.uuid,
                                taskUuid: nextSectionTask.uuid,
                            };
                        } else if (nextSection) {
                            return {
                                ...$currentSectionTask,
                                sectionUuid: nextSection.uuid,
                            };
                        } else {
                            return $currentSectionTask;
                        }
                    }
                    case "prev-section": {
                        if (prevSection && prevSectionTask) {
                            return {
                                ...$currentSectionTask,
                                kind: "task-selected",
                                sectionUuid: prevSection.uuid,
                                taskUuid: prevSectionTask.uuid,
                            };
                        } else if (prevSection) {
                            return {
                                ...$currentSectionTask,
                                sectionUuid: prevSection.uuid,
                            };
                        } else {
                            return $currentSectionTask;
                        }
                    }
                    case "prev-task": {
                        if (prevTask) {
                            return {
                                ...$currentSectionTask,
                                taskUuid: prevTask.uuid,
                            };
                        } else if (prevSection && lastTask) {
                            return {
                                ...$currentSectionTask,
                                sectionUuid: prevSection.uuid,
                                taskUuid: lastTask.uuid,
                            };
                        } else if (prevSection) {
                            return {
                                ...$currentSectionTask,
                                kind: "section-selected",
                                sectionUuid: prevSection.uuid,
                                taskUuid: undefined,
                            };
                        } else {
                            return $currentSectionTask;
                        }
                    }
                    case "next-task": {
                        if (nextTask) {
                            return {
                                ...$currentSectionTask,
                                taskUuid: nextTask.uuid,
                            };
                        } else if (nextSection && firstTask) {
                            return {
                                ...$currentSectionTask,
                                sectionUuid: nextSection.uuid,
                                taskUuid: firstTask.uuid,
                            };
                        } else if (nextSection) {
                            return {
                                ...$currentSectionTask,
                                kind: "section-selected",
                                sectionUuid: nextSection.uuid,
                                taskUuid: undefined,
                            };
                        } else {
                            return $currentSectionTask;
                        }
                    }
                }
            }
        },
    );
}
