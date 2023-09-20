import { moveTaskAfter } from "$lib/repository/workspace";
import type { MoveTaskModule } from "$lib/types/stores";
import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";

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
