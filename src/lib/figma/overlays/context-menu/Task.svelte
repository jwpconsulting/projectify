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

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import SubMenuDropdown from "$lib/figma/buttons/SubMenuDropdown.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import { goto } from "$lib/navigation";
    import { deleteTask } from "$lib/stores/dashboard";
    import { openDestructiveOverlay } from "$lib/stores/globalUi";
    import {
        moveToTop,
        moveToBottom,
        getTaskPosition,
    } from "$lib/stores/modules";
    import type { Task, WorkspaceBoardSection } from "$lib/types/workspace";
    import {
        getTaskUrl,
        getTaskUpdatesUrl,
        getDashboardWorkspaceBoardSectionUrl,
    } from "$lib/urls";
    import { copyToClipboard } from "$lib/utils/clipboard";

    export let task: Task;
    export let workspaceBoardSection: WorkspaceBoardSection;
    export let location: "dashboard" | "task";

    async function promptDeleteTask() {
        const { uuid } = workspaceBoardSection;
        await openDestructiveOverlay({ kind: "deleteTask" as const, task });
        await deleteTask(task);
        await goto(getDashboardWorkspaceBoardSectionUrl(uuid));
    }
</script>

<Layout>
    {#if location === "dashboard"}
        <ContextMenuButton
            kind={{
                kind: "a",
                href: getTaskUrl(task.uuid),
            }}
            label={$_("overlay.context-menu.task.open-task")}
            state="normal"
            icon={ArrowsExpand}
        />
    {/if}
    <SubMenuDropdown
        on:click={() => console.error("move to section not implemented")}
        label={$_("overlay.context-menu.task.move-to-section")}
        icon={SwitchVertical}
    />
    {#if location === "dashboard"}
        {#if getTaskPosition(workspaceBoardSection, task) !== "start"}
            <ContextMenuButton
                kind={{
                    kind: "button",
                    action: () => moveToTop(workspaceBoardSection, task),
                }}
                label={$_("overlay.context-menu.task.move-to-top")}
                state="normal"
                icon={SortAscending}
            />
        {/if}
        {#if getTaskPosition(workspaceBoardSection, task) !== "end"}
            <ContextMenuButton
                kind={{
                    kind: "button",
                    action: () => moveToBottom(workspaceBoardSection, task),
                }}
                label={$_("overlay.context-menu.task.move-to-bottom")}
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
        label={$_("overlay.context-menu.task.copy-link")}
        state="normal"
        icon={Duplicate}
    />
    {#if location === "dashboard"}
        <ContextMenuButton
            kind={{
                kind: "a",
                href: getTaskUpdatesUrl(task.uuid),
            }}
            label={$_("overlay.context-menu.task.go-to-updates")}
            state="normal"
            icon={ChatAlt}
        />
    {/if}
    <ContextMenuButton
        kind={{
            kind: "button",
            action: promptDeleteTask,
        }}
        label={$_("overlay.context-menu.task.delete-task")}
        state="normal"
        color="destructive"
        icon={Trash}
    />
</Layout>
