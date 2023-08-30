<script lang="ts">
    import {
        ArrowsExpand,
        ChatAlt,
        Duplicate,
        SortAscending,
        SortDescending,
        SwitchVertical,
        Trash,
    } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import { goto } from "$lib/navigation";
    import {
        getTaskUrl,
        getTaskUpdatesUrl,
        getDashboardWorkspaceBoardSectionUrl,
    } from "$lib/urls";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import SubMenuDropdown from "$lib/figma/buttons/SubMenuDropdown.svelte";
    import { deleteTask } from "$lib/stores/dashboard";
    import { openDestructiveOverlay } from "$lib/stores/globalUi";
    import type { MoveTaskModule } from "$lib/types/stores";
    import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";
    import { copyToClipboard } from "$lib/utils/clipboard";

    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSection;
    export let moveTaskModule: MoveTaskModule | undefined;
    export let location: "dashboard" | "task";

    async function promptDeleteTask() {
        const { uuid } = workspaceBoardSection;
        const target = {
            kind: "deleteTask" as const,
            task,
        };
        const result = await openDestructiveOverlay(target);
        if (result !== "success") {
            console.debug("User did not consent to task delete");
            return;
        }
        await deleteTask(task);
        await goto(getDashboardWorkspaceBoardSectionUrl(uuid));
    }
</script>

{#if location === "dashboard"}
    <ContextMenuButton
        kind={{
            kind: "a",
            href: getTaskUrl(task.uuid),
        }}
        label={$_("task-overlay.open-task")}
        state="normal"
        icon={ArrowsExpand}
    />
{/if}
<SubMenuDropdown
    on:click={() => console.error("move to section not implemented")}
    label={$_("task-overlay.move-to-section")}
    icon={SwitchVertical}
/>
{#if location === "dashboard"}
    {#if moveTaskModule?.moveToTop}
        <ContextMenuButton
            kind={{
                kind: "button",
                action: moveTaskModule.moveToTop,
            }}
            label={$_("task-overlay.move-to-top")}
            state="normal"
            icon={SortAscending}
        />
    {/if}
    {#if moveTaskModule?.moveToBottom}
        <ContextMenuButton
            kind={{
                kind: "button",
                action: moveTaskModule.moveToBottom,
            }}
            label={$_("task-overlay.move-to-bottom")}
            state="normal"
            icon={SortDescending}
        />
    {/if}
{/if}
<ContextMenuButton
    kind={{
        kind: "button",
        action: copyToClipboard.bind(
            null,
            new URL(getTaskUrl(task.uuid), document.baseURI).href
        ),
    }}
    label={$_("task-overlay.copy-link")}
    state="normal"
    icon={Duplicate}
/>
{#if location === "dashboard"}
    <ContextMenuButton
        kind={{
            kind: "a",
            href: getTaskUpdatesUrl(task.uuid),
        }}
        label={$_("task-overlay.go-to-updates")}
        state="normal"
        icon={ChatAlt}
    />
{/if}
<ContextMenuButton
    kind={{
        kind: "button",
        action: promptDeleteTask,
    }}
    label={$_("task-overlay.delete-task")}
    state="normal"
    color="destructive"
    icon={Trash}
/>
