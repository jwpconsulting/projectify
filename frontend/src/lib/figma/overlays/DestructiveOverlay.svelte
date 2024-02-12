<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import {
        rejectDestructiveOverlay,
        resolveDestructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { DestructiveOverlayType } from "$lib/types/ui";
    import { getDisplayName } from "$lib/types/user";

    export let target: DestructiveOverlayType;

    let title: string;
    let body: string;
    let warning: string;
    let buttonLabel: string;
    $: {
        switch (target.kind) {
            case "deleteLabel":
                title = $_("overlay.destructive.delete-label.title");
                body = $_("overlay.destructive.delete-label.body", {
                    values: { label: target.label.name },
                });
                warning = $_("overlay.destructive.delete-label.warning");
                buttonLabel = $_("overlay.destructive.delete-label.button");
                break;
            case "deleteWorkspaceUser":
                title = $_("overlay.destructive.delete-workspace-user.title");
                body = $_("overlay.destructive.delete-workspace-user.body", {
                    values: {
                        workspaceUser: getDisplayName(
                            target.workspaceUser.user,
                        ),
                    },
                });
                warning = $_(
                    "overlay.destructive.delete-workspace-user.warning",
                );
                buttonLabel = $_(
                    "overlay.destructive.delete-workspace-user.button",
                );
                break;
            case "deleteWorkspaceBoardSection":
                title = $_(
                    "overlay.destructive.delete-workspace-board-section.title",
                );
                body = $_(
                    "overlay.destructive.delete-workspace-board-section.body",
                    {
                        values: {
                            workspaceBoardSection:
                                target.workspaceBoardSection.title,
                        },
                    },
                );
                warning = $_(
                    "overlay.destructive.delete-workspace-board-section.warning",
                );
                buttonLabel = $_(
                    "overlay.destructive.delete-workspace-board-section.button",
                );
                break;
            case "deleteTask":
                title = $_("overlay.destructive.delete-task.title");
                body = $_("overlay.destructive.delete-task.body", {
                    values: { task: target.task.title },
                });
                warning = $_("overlay.destructive.delete-task.warning");
                buttonLabel = $_("overlay.destructive.delete-task.button");
                break;
            case "deleteSelectedTasks":
                title = $_("overlay.destructive.delete-selected-tasks.title");
                // XXX not used, and even if, we should show all task titles
                // instead of just a count
                body = $_("overlay.destructive.delete-selected-tasks.body", {
                    values: { count: target.tasks.length.toString() },
                });
                warning = $_(
                    "overlay.destructive.delete-selected-tasks.warning",
                );
                buttonLabel = $_(
                    "overlay.destructive.delete-selected-tasks.button",
                );
                break;
            case "archiveWorkspaceBoard":
                title = $_(
                    "overlay.destructive.archive-workspace-board.title",
                );
                body = $_("overlay.destructive.archive-workspace-board.body", {
                    values: { workspaceBoard: target.workspaceBoard.title },
                });
                warning = $_(
                    "overlay.destructive.archive-workspace-board.warning",
                );
                buttonLabel = $_(
                    "overlay.destructive.archive-workspace-board.button",
                );
                break;
            case "deleteWorkspaceBoard":
                title = $_("overlay.destructive.delete-workspace-board.title");
                body = $_("overlay.destructive.delete-workspace-board.body", {
                    values: { workspaceBoard: target.workspaceBoard.title },
                });
                warning = $_(
                    "overlay.destructive.delete-workspace-board.warning",
                );
                buttonLabel = $_(
                    "overlay.destructive.delete-workspace-board.button",
                );
                break;
        }
    }
</script>

<div
    class="flex w-full max-w-lg flex-col items-center gap-4 rounded-lg bg-foreground p-8"
>
    <div class="text-center text-3xl font-bold text-base-content">{title}</div>
    <div
        class="flex w-full flex-col items-center gap-8 border-t border-border pt-2"
    >
        <div
            class="text-normal w-full overflow-auto text-center text-base-content"
        >
            <p>{body}</p>
            <p class="text-destructive">{warning}</p>
        </div>
        <div class="flex w-full flex-row items-center justify-center gap-2">
            <Button
                style={{ kind: "secondary" }}
                size="medium"
                color="blue"
                grow
                action={{ kind: "button", action: rejectDestructiveOverlay }}
                label={$_("overlay.destructive.cancel")}
            />
            <Button
                style={{ kind: "primary" }}
                size="medium"
                color="red"
                grow
                action={{ kind: "button", action: resolveDestructiveOverlay }}
                label={buttonLabel}
            />
        </div>
    </div>
</div>
