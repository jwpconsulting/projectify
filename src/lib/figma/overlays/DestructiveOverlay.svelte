<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import {
        closeDestructiveOverlay,
        performDestructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { DestructiveOverlayType } from "$lib/types/ui";

    export let target: DestructiveOverlayType;

    $: title = {
        deleteLabel: $_("destructive-overlay.delete-label"),
        deleteMember: $_("destructive-overlay.delete-member"),
        deleteSection: $_("destructive-overlay.delete-section"),
        deleteTask: $_("destructive-overlay.delete-task"),
        deleteSelectedTasks: $_("destructive-overlay.delete-selected-tasks"),
        archiveBoard: $_("destructive-overlay.archive-board"),
        deleteBoard: $_("destructive-overlay.delete-board"),
    }[target.kind];
    $: body1 = {
        deleteLabel: $_("destructive-overlay.delete-label-body-1"),
        deleteMember: $_("destructive-overlay.delete-member-body-1"),
        deleteSection: $_("destructive-overlay.delete-section-body-1"),
        deleteTask: $_("destructive-overlay.delete-task-body-1"),
        deleteSelectedTasks: $_(
            "destructive-overlay.delete-selected-tasks-body-1"
        ),
        archiveBoard: $_("destructive-overlay.archive-board-body-1"),
        deleteBoard: $_("destructive-overlay.delete-board-body-1"),
    }[target.kind];
    $: body2 = {
        deleteLabel: $_("destructive-overlay.delete-label-body-2"),
        deleteMember: $_("destructive-overlay.delete-member-body-2"),
        deleteSection: $_("destructive-overlay.delete-section-body-2"),
        deleteTask: $_("destructive-overlay.delete-task-body-2"),
        deleteSelectedTasks: $_(
            "destructive-overlay.delete-selected-tasks-body-2"
        ),
        archiveBoard: $_("destructive-overlay.archive-board-body-2"),
        deleteBoard: $_("destructive-overlay.delete-board-body-2"),
    }[target.kind];
    $: warning = {
        deleteLabel: $_("destructive-overlay.delete-label-body-warning"),
        deleteMember: $_("destructive-overlay.delete-member-body-warning"),
        deleteSection: $_("destructive-overlay.delete-section-body-warning"),
        deleteTask: $_("destructive-overlay.delete-task-body-warning"),
        deleteSelectedTasks: $_(
            "destructive-overlay.delete-selected-tasks-body-warning"
        ),
        archiveBoard: $_("destructive-overlay.archive-board-body-warning"),
        deleteBoard: $_("destructive-overlay.delete-board-body-warning"),
    }[target.kind];
    $: buttonLabel = {
        deleteLabel: $_("destructive-overlay.delete-label-button"),
        deleteMember: $_("destructive-overlay.delete-member-button"),
        deleteSection: $_("destructive-overlay.delete-section-button"),
        deleteTask: $_("destructive-overlay.delete-task-button"),
        deleteSelectedTasks: $_(
            "destructive-overlay.delete-selected-tasks-button"
        ),
        archiveBoard: $_("destructive-overlay.archive-board-button"),
        deleteBoard: $_("destructive-overlay.delete-board-button"),
    }[target.kind];
    let targetName: string;
    $: {
        switch (target.kind) {
            case "deleteLabel":
                targetName = target.label.name;
                break;
            case "deleteMember":
                targetName =
                    target.workspaceUser.user.full_name ??
                    target.workspaceUser.user.email;
                break;
            case "deleteSection":
                targetName = target.workspaceBoardSection.title;
                break;
            case "deleteTask":
                targetName = target.task.title;
                break;
            case "deleteSelectedTasks":
                targetName = target.tasks.length.toString();
                break;
            case "archiveBoard":
                targetName = target.workspaceBoard.title;
                break;
            case "deleteBoard":
                targetName = target.workspaceBoard.title;
                break;
        }
    }
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
                {body1}<span class="text-primary">{targetName}</span>{body2}
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
                action={{ kind: "button", action: closeDestructiveOverlay }}
                label={$_("destructive-overlay.cancel")}
            />
            <Button
                style={{ kind: "primary" }}
                size="medium"
                color="red"
                action={{ kind: "button", action: performDestructiveOverlay }}
                label={buttonLabel}
            />
        </div>
    </div>
</div>
