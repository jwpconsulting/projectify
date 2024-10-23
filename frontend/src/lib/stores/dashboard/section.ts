// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
import { derived } from "svelte/store";
import type { Readable } from "svelte/store";

import { selectedLabels } from "$lib/stores/dashboard/labelFilter";
import { currentProject } from "$lib/stores/dashboard/project";
import { selectedTeamMember } from "$lib/stores/dashboard/teamMemberFilter";
import type {
    LabelSelection,
    TasksPerUser,
    TeamMemberSelection,
} from "$lib/types/ui";
import type { Label, ProjectDetailSection } from "$lib/types/workspace";

interface CurrentFilter {
    labels: LabelSelection;
    teamMember: TeamMemberSelection;
    sections: readonly ProjectDetailSection[];
}

function filterSectionsTasks(
    currentFilter: CurrentFilter,
): readonly ProjectDetailSection[] {
    type Task = ProjectDetailSection["tasks"][number];
    let sections: readonly ProjectDetailSection[] = currentFilter.sections;
    if (currentFilter.labels.kind === "noLabel") {
        // TODO filter by no label? Justus 2023-04-04
        // eslint-disable-next-line
        // Maybe: return sections;
    } else if (currentFilter.labels.kind === "allLabels") {
        // TODO what to do here?
        // eslint-disable-next-line
        // Maybe: return sections;
    } else {
        const labelUuids = [...currentFilter.labels.labelUuids.keys()];

        sections = sections.map((section) => {
            const tasks = section.tasks.filter((task: Task) => {
                return (
                    task.labels.findIndex((l: Label) =>
                        labelUuids.find((labelUuid) => l.uuid === labelUuid)
                            ? true
                            : false,
                    ) >= 0
                );
            });

            return { ...section, tasks };
        });
    }

    const teamMemberSelection = currentFilter.teamMember;
    if (teamMemberSelection.kind !== "allTeamMembers") {
        sections = sections.map((section) => {
            const tasks = section.tasks.filter((task: Task) => {
                if (teamMemberSelection.kind === "unassigned") {
                    return !task.assignee;
                } else {
                    return task.assignee
                        ? teamMemberSelection.teamMemberUuids.has(
                              task.assignee.uuid,
                          )
                        : false;
                }
            });

            return { ...section, tasks };
        });
    }

    return sections;
}

export const currentSections = derived<
    [typeof selectedLabels, typeof selectedTeamMember, typeof currentProject],
    readonly ProjectDetailSection[] | undefined
>(
    [selectedLabels, selectedTeamMember, currentProject],
    ([$selectedLabels, $selectedTeamMember, $currentProject], set) => {
        if (!$currentProject.value) {
            set(undefined);
            return;
        }
        const sections = $currentProject.value.sections;
        set(
            filterSectionsTasks({
                labels: $selectedLabels,
                teamMember: $selectedTeamMember,
                sections,
            }),
        );
    },
    undefined,
);

export const tasksPerUser: Readable<TasksPerUser> = derived<
    Readable<readonly ProjectDetailSection[] | undefined>,
    TasksPerUser
>(
    currentSections,
    ($currentSections: readonly ProjectDetailSection[] | undefined, set) => {
        if ($currentSections === undefined) {
            return;
        }
        const assigned = new Map<string, number>();
        let unassigned = 0;
        $currentSections.forEach((section: ProjectDetailSection) => {
            section.tasks.forEach((task) => {
                const uuid = task.assignee?.uuid;
                if (uuid === undefined) {
                    unassigned = unassigned + 1;
                    return;
                }
                const current = assigned.get(uuid) ?? 0;
                assigned.set(uuid, current + 1);
            });
        });
        set({ unassigned, assigned });
    },
    { unassigned: 0, assigned: new Map<string, number>() },
);
