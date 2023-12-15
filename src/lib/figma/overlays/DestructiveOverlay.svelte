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

    let bodyValues: { values: Record<string, string> };
    $: {
        switch (target.kind) {
            case "deleteLabel":
                bodyValues = { values: { label: target.label.name } };
                break;
            case "deleteWorkspaceUser":
                // TODO use proper name interpolation method to be found
                // somewhere in utils
                bodyValues = {
                    values: {
                        workspaceUser: getDisplayName(
                            target.workspaceUser.user
                        ),
                    },
                };
                break;
            case "deleteWorkspaceBoardSection":
                bodyValues = {
                    values: {
                        workspaceBoardSection:
                            target.workspaceBoardSection.title,
                    },
                };
                break;
            case "deleteTask":
                bodyValues = { values: { task: target.task.title } };
                break;
            case "deleteSelectedTasks":
                // XXX not used, and even if, we should show all task titles
                // instead of just a count
                bodyValues = {
                    values: { count: target.tasks.length.toString() },
                };
                break;
            case "archiveWorkspaceBoard":
                bodyValues = {
                    values: { workspaceBoard: target.workspaceBoard.title },
                };
                break;
            case "deleteWorkspaceBoard":
                bodyValues = {
                    values: { workspaceBoard: target.workspaceBoard.title },
                };
                break;
        }
    }

    $: title = {
        deleteLabel: $_("overlay.destructive.delete-label.title"),
        deleteWorkspaceUser: $_(
            "overlay.destructive.delete-workspace-user.title"
        ),
        deleteWorkspaceBoardSection: $_(
            "overlay.destructive.delete-section.title"
        ),
        deleteTask: $_("overlay.destructive.delete-task.title"),
        deleteSelectedTasks: $_(
            "overlay.destructive.delete-selected-tasks.title"
        ),
        archiveWorkspaceBoard: $_("overlay.destructive.archive-board.title"),
        deleteWorkspaceBoard: $_("overlay.destructive.delete-board.title"),
    }[target.kind];
    $: body = {
        deleteLabel: $_("overlay.destructive.delete-label.body", bodyValues),
        deleteWorkspaceUser: $_(
            "overlay.destructive.delete-workspace-user.body",
            bodyValues
        ),
        deleteWorkspaceBoardSection: $_(
            "overlay.destructive.delete-section.body",
            bodyValues
        ),
        deleteTask: $_("overlay.destructive.delete-task.body", bodyValues),
        deleteSelectedTasks: $_(
            "overlay.destructive.delete-selected-tasks.body",
            bodyValues
        ),
        archiveWorkspaceBoard: $_(
            "overlay.destructive.archive-board.body",
            bodyValues
        ),
        deleteWorkspaceBoard: $_(
            "overlay.destructive.delete-board.body",
            bodyValues
        ),
    }[target.kind];
    $: warning = {
        deleteLabel: $_("overlay.destructive.delete-label.warning"),
        deleteWorkspaceUser: $_(
            "overlay.destructive.delete-workspace-user.warning"
        ),
        deleteWorkspaceBoardSection: $_(
            "overlay.destructive.delete-section.warning"
        ),
        deleteTask: $_("overlay.destructive.delete-task.warning"),
        deleteSelectedTasks: $_(
            "overlay.destructive.delete-selected-tasks.warning"
        ),
        archiveWorkspaceBoard: $_("overlay.destructive.archive-board.warning"),
        deleteWorkspaceBoard: $_("overlay.destructive.delete-board.warning"),
    }[target.kind];
    $: buttonLabel = {
        deleteLabel: $_("overlay.destructive.delete-label.button"),
        deleteWorkspaceUser: $_(
            "overlay.destructive.delete-workspace-user.button"
        ),
        deleteWorkspaceBoardSection: $_(
            "overlay.destructive.delete-section.button"
        ),
        deleteTask: $_("overlay.destructive.delete-task.button"),
        deleteSelectedTasks: $_(
            "overlay.destructive.delete-selected-tasks.button"
        ),
        archiveWorkspaceBoard: $_("overlay.destructive.archive-board.button"),
        deleteWorkspaceBoard: $_("overlay.destructive.delete-board.button"),
    }[target.kind];
</script>

<div
    class="flex w-[500px] flex-col items-center gap-4 rounded-lg bg-foreground p-8"
>
    <div class="text-3xl font-bold text-base-content">
        {title}
    </div>
    <div class="flex flex-col items-center gap-8 border-t border-border pt-2">
        <div class="text-normal text-center text-base-content">
            <p>
                <!-- {body1}<span class="text-primary">{targetName}</span>{body2}
                     -->
                {body}
            </p>
            <p class="text-destructive">
                {warning}
            </p>
        </div>
        <div class="flex flex-row items-center justify-center gap-2">
            <!-- TODO make buttons grow -->
            <Button
                style={{ kind: "secondary" }}
                size="medium"
                color="blue"
                action={{ kind: "button", action: rejectDestructiveOverlay }}
                label={$_("overlay.destructive.cancel")}
            />
            <Button
                style={{ kind: "primary" }}
                size="medium"
                color="red"
                action={{ kind: "button", action: resolveDestructiveOverlay }}
                label={buttonLabel}
            />
        </div>
    </div>
</div>
