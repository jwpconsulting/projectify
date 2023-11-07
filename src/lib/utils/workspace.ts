/*
 * Workspace related utility function
 */
import type { SubTask } from "$lib/types/workspace";

/*
 * Calculate ratio of completed sub tasks to all sub tasks within a task.
 *
 * Handles sub_tasks being absent cleanly.
 */
export function getSubTaskProgress(sub_tasks: SubTask[]): number | undefined {
    // TODO but really, we should have a task where sub_tasks is set to
    // mandatory present, checking for undefined is tedious.
    if (sub_tasks.length === 0) {
        return undefined;
    }
    const completed = sub_tasks.filter((subTask) => subTask.done).length;
    const total = sub_tasks.length;
    if (completed == total) {
        return 1;
    }
    return completed / total;
}
