import { writable } from "svelte/store";

import { moveTaskAfter } from "$lib/repository/workspace";
import {
    createLabelSearch,
    createLabelSearchResults,
    currentWorkspaceLabels,
} from "$lib/stores/dashboard";
import type { LabelSearchModule, MoveTaskModule } from "$lib/types/stores";
import type { LabelSelection, LabelSelectionInput } from "$lib/types/ui";
import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";

export function createLabelSearchModule(
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
    const search = createLabelSearch();
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
        async createLabel() {
            await new Promise(console.error);
            throw new Error("Not implemented");
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
    const taskIndex = tasks.findIndex((t) => t.uuid == taskUuid);
    if (taskIndex === -1) {
        throw new Error("task was not found in tasks");
    }
    const isFirstTask = taskIndex === 0;
    const isLastTask = taskIndex === tasks.length - 1;
    const lastTask = !isLastTask ? tasks[tasks.length - 1] : undefined;

    const moveToTop = isFirstTask
        ? undefined
        : moveTaskAfter.bind(null, taskUuid, workspaceBoardSectionUuid, null);
    const moveToBottom = lastTask
        ? moveTaskAfter.bind(
              null,
              taskUuid,
              workspaceBoardSectionUuid,
              lastTask.uuid
          )
        : undefined;

    return {
        moveToTop,
        moveToBottom,
        moveToWorkspaceBoardSection: ({ uuid }: WorkspaceBoardSection) =>
            moveTaskAfter(taskUuid, uuid),
    };
}
