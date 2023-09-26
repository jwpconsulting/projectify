import { moveTaskAfter } from "$lib/repository/workspace";
import type { MoveTaskModule } from "$lib/types/stores";
import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";
import { unwrap } from "$lib/utils/type";

type TaskPosition = "start" | "within" | "end" | "outside";

function getTaskPosition(
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

export function createMoveTaskModule(
    workspaceBoardSection: WorkspaceBoardSection,
    task: Task
): MoveTaskModule {
    const tasks = unwrap(workspaceBoardSection.tasks, "Expected tasks");
    const position = getTaskPosition(workspaceBoardSection, task);
    const lastTask = tasks[tasks.length - 1];

    const moveToTop =
        position === "start"
            ? undefined
            : moveTaskAfter.bind(
                  null,
                  task.uuid,
                  workspaceBoardSection.uuid,
                  null
              );
    const moveToBottom =
        position === "end"
            ? undefined
            : moveTaskAfter.bind(
                  null,
                  task.uuid,
                  workspaceBoardSection.uuid,
                  lastTask.uuid
              );

    return {
        moveToTop,
        moveToBottom,
        moveToWorkspaceBoardSection: ({ uuid }: WorkspaceBoardSection) =>
            moveTaskAfter(task.uuid, uuid),
    };
}
