// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
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
    sub_tasks: Partial<Pick<SubTask, "done">>[],
): number | undefined {
    if (sub_tasks.length === 0) {
        return undefined;
    }
    const completed = sub_tasks.filter(
        (subTask) => subTask.done === true,
    ).length;
    const total = sub_tasks.length;
    if (completed == total) {
        return 1;
    }
    return completed / total;
}
