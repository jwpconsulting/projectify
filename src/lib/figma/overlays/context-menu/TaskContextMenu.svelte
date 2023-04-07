<script lang="ts">
    import { _ } from "svelte-i18n";
    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import SubMenuDropdown from "$lib/figma/buttons/SubMenuDropdown.svelte";
    import {
        ArrowsExpand,
        ChatAlt,
        Duplicate,
        SortAscending,
        SortDescending,
        SwitchVertical,
        Trash,
    } from "@steeze-ui/heroicons";
    import type { Task } from "$lib/types/workspace";

    export let task: Task;
    export let location: "dashboard" | "task";
    // TODO
    console.log(task);
</script>

{#if location === "dashboard"}
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("open task not implemented"),
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
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("move to top not implemented"),
        }}
        label={$_("task-overlay.move-to-top")}
        state="normal"
        icon={SortAscending}
    />
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("move to bottom not implemented"),
        }}
        label={$_("task-overlay.move-to-bottom")}
        state="normal"
        icon={SortDescending}
    />
{/if}
<ContextMenuButton
    kind={{
        kind: "button",
        action: () => console.error("copy link not implemented"),
    }}
    label={$_("task-overlay.copy-link")}
    state="normal"
    icon={Duplicate}
/>
{#if location === "dashboard"}
    <ContextMenuButton
        kind={{
            kind: "button",
            action: () => console.error("go to updates not implemented"),
        }}
        label={$_("task-overlay.go-to-updates")}
        state="normal"
        icon={ChatAlt}
    />
{/if}
<ContextMenuButton
    kind={{
        kind: "button",
        action: () => console.error("delete task not implemented"),
    }}
    label={$_("task-overlay.delete-task")}
    state="normal"
    color="destructive"
    icon={Trash}
/>
