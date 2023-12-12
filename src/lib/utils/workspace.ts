/*
 * Workspace related utility function
 */

import type { SubTask } from "$lib/types/workspace";

/*
 * Calculate ratio of completed sub tasks to all sub tasks within a task.
 *
 * Handles sub_tasks being absent cleanly.
 */
export function getSubTaskProgress(
    // We are only interested in done, and other properties may not
    // be given when creating new sub tasks
    sub_tasks: Partial<Pick<SubTask, "done">>[]
): number | undefined {
    if (sub_tasks.length === 0) {
        return undefined;
    }
    const completed = sub_tasks.filter(
        (subTask) => subTask.done === true
    ).length;
    const total = sub_tasks.length;
    if (completed == total) {
        return 1;
    }
    return completed / total;
}
