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

export async function moveToBottom(
    workspaceBoardSection: WorkspaceBoardSection,
    task: Task
) {
    const tasks = unwrap(workspaceBoardSection.tasks, "Expected tasks");
    const lastTask = unwrap(tasks.at(-1), "Expected lastTask");
    await moveTaskAfter(task.uuid, workspaceBoardSection.uuid, lastTask.uuid);
}
