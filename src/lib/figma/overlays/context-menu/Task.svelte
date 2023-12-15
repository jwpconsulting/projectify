<script lang="ts">
    import {
        ArrowsExpand,
        ChatAlt,
        ChevronDown,
        ChevronUp,
        Duplicate,
        SortAscending,
        SortDescending,
        SwitchVertical,
        Trash,
    } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import { goto } from "$lib/navigation";
    import { deleteTask } from "$lib/stores/dashboard";
    import { openDestructiveOverlay } from "$lib/stores/globalUi";
    import {
        moveToTop,
        moveToBottom,
        getTaskPosition,
    } from "$lib/stores/modules";
    import type {
        TaskWithWorkspaceBoardSection,
        WorkspaceBoardDetail,
        WorkspaceBoardSection,
    } from "$lib/types/workspace";
    import {
        getTaskUrl,
        getTaskUpdatesUrl,
        getDashboardWorkspaceBoardSectionUrl,
    } from "$lib/urls";
    import { copyToClipboard } from "$lib/utils/clipboard";

    export let task: TaskWithWorkspaceBoardSection;
    export let workspaceBoardSection: WorkspaceBoardSection;
    export let workspaceBoard: WorkspaceBoardDetail | undefined;
    export let location: "dashboard" | "task";

    async function promptDeleteTask() {
        const { uuid } = workspaceBoardSection;
        await openDestructiveOverlay({ kind: "deleteTask" as const, task });
        await deleteTask(task);
        await goto(getDashboardWorkspaceBoardSectionUrl(uuid));
    }

    let moveToSectionOpened = false;

    function toggleMoveToSection() {
        moveToSectionOpened = !moveToSectionOpened;
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
    <ContextMenuButton
        kind={{ kind: "button", action: toggleMoveToSection }}
        label={$_("overlay.context-menu.task.move-to-section")}
        state="normal"
        closeOnInteract={false}
        icon={SwitchVertical}
        iconRight={moveToSectionOpened ? ChevronUp : ChevronDown}
    />
    {#if location === "dashboard"}
        {#if getTaskPosition(workspaceBoardSection, task).kind !== "start"}
            <ContextMenuButton
                kind={{
                    kind: "button",
                    action: () =>
                        moveToTop(workspaceBoardSection, task, { fetch }),
                }}
                label={$_("overlay.context-menu.task.move-to-top")}
                state="normal"
                icon={SortAscending}
            />
        {/if}
        {#if getTaskPosition(workspaceBoardSection, task).kind !== "end"}
            <ContextMenuButton
                kind={{
                    kind: "button",
                    action: () =>
                        moveToBottom(workspaceBoardSection, task, { fetch }),
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
