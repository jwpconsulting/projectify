import { moveTaskAfter } from "$lib/repository/workspace";
import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

type TaskPosition = "start" | "within" | "end" | "outside";

export function getTaskPosition(
    workspaceBoardSection: WorkspaceBoardSection,
    task: Task
): TaskPosition {
    const tasks = unwrap(workspaceBoardSection.tasks, "Expected tasks");
    const taskIndex = tasks.findIndex((t) => t.uuid == task.uuid);
    const lastIndex = tasks.length - 1;
    switch (taskIndex) {
        case -1:
            return "outside";
        case 0:
            return "start";
        case lastIndex:
            return "end";
        default:
            return "within";
    }
}

export async function moveToTop(
    workspaceBoardSection: WorkspaceBoardSection,
    task: Task
) {
    await moveTaskAfter(task.uuid, workspaceBoardSection.uuid, null);
}

export async function moveUp(
    workspaceBoardSection: WorkspaceBoardSection,
    task: Task
) {
    const tasks = unwrap(workspaceBoardSection.tasks, "Expected tasks");
    const position = getTaskPosition(workspaceBoardSection, task);
    if (!(position === "within" || position === "end")) {
        throw new Error("Expected task to be within or at end");
    }
    const prevTask = unwrap(
        tasks.at(tasks.indexOf(task) - 1),
        "Expected prevTask"
    );
    await moveTaskAfter(task.uuid, workspaceBoardSection.uuid, prevTask.uuid);
}

export async function moveToBottom(
    workspaceBoardSection: WorkspaceBoardSection,
    task: Task
) {
    const tasks = unwrap(workspaceBoardSection.tasks, "Expected tasks");
    const lastTask = unwrap(tasks.at(-1), "Expected lastTask");
    await moveTaskAfter(task.uuid, workspaceBoardSection.uuid, lastTask.uuid);
}

export async function moveDown(
    workspaceBoardSection: WorkspaceBoardSection,
    task: Task
) {
    const position = getTaskPosition(workspaceBoardSection, task);
    if (!(position === "start" || position === "within")) {
        throw new Error("Expected task to be at start or within");
    }
    const tasks = unwrap(workspaceBoardSection.tasks, "Expected tasks");
    const nextTask = unwrap(
        tasks.at(tasks.indexOf(task) + 1),
        "Expected nextTask"
    );
    await moveTaskAfter(task.uuid, workspaceBoardSection.uuid, nextTask.uuid);
}
