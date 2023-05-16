import { writable } from "svelte/store";
import {
    moveTaskAfter,
    createLabel as repositoryCreateLabel,
    moveWorkspaceBoardSection,
} from "$lib/repository/workspace";
import {
    createLabelSearchResults,
    currentWorkspaceLabels,
} from "$lib/stores/dashboard";
import {
    toggleWorkspaceBoardSectionOpen,
    workspaceBoardSectionClosed,
} from "$lib/stores/dashboard/ui";
import type {
    Workspace,
    Task,
    WorkspaceBoardSection,
} from "$lib/types/workspace";

import type {
    LabelSearchModule,
    MoveTaskModule,
    WorkspaceBoardSectionModule,
} from "$lib/types/stores";
import type { LabelSelection, LabelSelectionInput } from "$lib/types/ui";

export function createLabelSearchModule(
    workspace: Workspace,
    task: Task | null,
    selectCallback: (labelUuid: string, selected: boolean) => void
): LabelSearchModule {
    const labelSelected: LabelSelection =
        task?.labels && task.labels.length > 0
            ? {
                  kind: "labels",
                  labelUuids: new Set(task.labels.map((l) => l.uuid)),
              }
            : { kind: "noLabel" };
    const search = writable("");
    const selectOrDeselectLabel = (
        select: boolean,
        labelSelectionInput: LabelSelectionInput
    ) => {
        const { kind } = labelSelectionInput;
        if (kind === "noLabel") {
            console.error("No API for removing all labels");
            throw new Error("TODO");
        } else if (kind === "allLabels") {
            // XXX Clearly, allLabels only makes sense for side nav, not when
            // assigning labels to tasks
            console.error("No API for assigning all labels");
            throw new Error("TODO");
        } else {
            const { labelUuid } = labelSelectionInput;
            selectCallback(labelUuid, select);
        }
    };
    return {
        select: (labelSelectionInput: LabelSelectionInput) => {
            selectOrDeselectLabel(true, labelSelectionInput);
        },
        deselect: (labelSelectionInput: LabelSelectionInput) => {
            selectOrDeselectLabel(false, labelSelectionInput);
        },
        selected: writable<LabelSelection>(labelSelected),
        search,
        searchResults: createLabelSearchResults(
            currentWorkspaceLabels,
            search
        ),
        async createLabel(color: number, name: string) {
            await repositoryCreateLabel(workspace, name, color);
        },
    };
}

export function createMoveTaskModule(
    { uuid: workspaceBoardSectionUuid }: WorkspaceBoardSection,
    task: Task,
    tasks: Task[]
): MoveTaskModule {
    if (!tasks.length) {
        throw new Error("Expected tasks");
    }
    const { uuid: taskUuid } = task;
    const lastTask = tasks[tasks.length - 1];
    const { uuid: afterTaskUuid } = lastTask;

    return {
        moveToTop: moveTaskAfter.bind(
            null,
            taskUuid,
            workspaceBoardSectionUuid,
            null
        ),
        moveToBottom: moveTaskAfter.bind(
            null,
            taskUuid,
            workspaceBoardSectionUuid,
            afterTaskUuid
        ),
        moveToWorkspaceBoardSection: ({ uuid }: WorkspaceBoardSection) =>
            moveTaskAfter(taskUuid, uuid),
    };
}

export function createWorkspaceBoardSectionModule(
    workspaceBoardSections: WorkspaceBoardSection[],
    section: WorkspaceBoardSection
): WorkspaceBoardSectionModule {
    // XXX very convoluted, just to get a conditionally assigned fn...
    const sectionIndex: number = workspaceBoardSections.findIndex(
        (s: WorkspaceBoardSection) => s.uuid == section.uuid
    );
    const previousIndex = sectionIndex > 0 ? sectionIndex - 1 : undefined;
    const nextIndex =
        sectionIndex < workspaceBoardSections.length - 1
            ? sectionIndex + 1
            : undefined;
    const previousSection: WorkspaceBoardSection | undefined =
        previousIndex !== undefined
            ? workspaceBoardSections[previousIndex]
            : undefined;
    const nextSection: WorkspaceBoardSection | undefined =
        nextIndex !== undefined
            ? workspaceBoardSections[nextIndex]
            : undefined;

    const switchWithPreviousSection = previousSection
        ? async () => {
              await moveWorkspaceBoardSection(section, previousSection._order);
          }
        : undefined;
    const switchWithNextSection = nextSection
        ? async () => {
              await moveWorkspaceBoardSection(section, nextSection._order);
          }
        : undefined;

    const workspaceBoardSectionModule: WorkspaceBoardSectionModule = {
        workspaceBoardSectionClosed,
        toggleWorkspaceBoardSectionOpen,
        switchWithPrevSection: switchWithPreviousSection,
        switchWithNextSection,
    };
    return workspaceBoardSectionModule;
}
