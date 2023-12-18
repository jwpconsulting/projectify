// TODO consider putting this either in repository or make it part of the
// task store file
import {
    moveTaskAfterTask,
    moveTaskToWorkspaceBoardSection,
} from "$lib/repository/workspace";
import type { RepositoryContext } from "$lib/types/repository";
import type {
    Task,
    TaskWithWorkspaceBoardSection,
    WorkspaceBoardSectionWithTasks,
} from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

type TaskPosition =
    | { kind: "start"; position: 0; isOnly: boolean }
    | { kind: "within"; position: number }
    | { kind: "end"; position: number }
    | { kind: "outside" };

export function getTaskPosition(
    workspaceBoardSection: WorkspaceBoardSectionWithTasks,
    task: Task,
): TaskPosition {
    const { tasks } = workspaceBoardSection;
    const taskIndex = tasks.findIndex((t) => t.uuid == task.uuid);
    const lastIndex = tasks.length - 1;
    switch (taskIndex) {
        case -1:
            return { kind: "outside" };
        case 0:
            return { kind: "start", position: 0, isOnly: tasks.length === 1 };
        case lastIndex:
            return { kind: "end", position: lastIndex };
        default:
            return { kind: "within", position: taskIndex };
    }
}

export async function moveToTop(
    workspaceBoardSection: WorkspaceBoardSectionWithTasks,
    task: TaskWithWorkspaceBoardSection,
    repositoryContext: RepositoryContext,
) {
    await moveTaskToWorkspaceBoardSection(
        task,
        workspaceBoardSection,
        repositoryContext,
    );
}

export async function moveToBottom(
    workspaceBoardSection: WorkspaceBoardSectionWithTasks,
    task: Task,
    repositoryContext: RepositoryContext,
) {
    const tasks = unwrap(workspaceBoardSection.tasks, "Expected tasks");
    const lastTask = unwrap(tasks.at(-1), "Expected lastTask");
    await moveTaskAfterTask(task, lastTask, repositoryContext);
}

export async function moveUp(
    workspaceBoardSection: WorkspaceBoardSectionWithTasks,
    task: Task,
    repositoryContext: RepositoryContext,
) {
    const tasks = unwrap(workspaceBoardSection.tasks, "Expected tasks");
    const position = getTaskPosition(workspaceBoardSection, task);
    if (!(position.kind === "within" || position.kind === "end")) {
        throw new Error("Expected task to be within or at end");
    }
    const prevTask = unwrap(
        tasks.at(position.position - 1),
        "Expected prevTask",
    );
    await moveTaskAfterTask(task, prevTask, repositoryContext);
}

export async function moveDown(
    workspaceBoardSection: WorkspaceBoardSectionWithTasks,
    task: Task,
    repositoryContext: RepositoryContext,
) {
    const position = getTaskPosition(workspaceBoardSection, task);
    if (!(position.kind === "start" || position.kind === "within")) {
        throw new Error("Expected task to be at start or within");
    }
    const tasks = unwrap(workspaceBoardSection.tasks, "Expected tasks");
    const nextTask = unwrap(
        tasks.at(position.position + 1),
        "Expected nextTask",
    );
    await moveTaskAfterTask(task, nextTask, repositoryContext);
}
