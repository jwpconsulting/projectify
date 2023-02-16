<script lang="ts">
    import { _ } from "svelte-i18n";
    import TabElement from "$lib/figma/buttons/TabElement.svelte";
    import type {
        TaskUpdateBarKind,
        TaskUpdateBarState,
    } from "$lib/figma/types";

    export let kind: TaskUpdateBarKind;
    export let state: TaskUpdateBarState;
</script>

{#if kind === "mobile"}
    <div class="flex flex-row">
        {#if state === "task"}
            <TabElement href="#" label={$_("task")} active />
        {:else}
            <TabElement href="#" label={$_("updates")} active />
        {/if}
        <div class="grow border-b-2 border-base-content" />
    </div>
{:else}
    <div class="flex flex-row">
        <TabElement href="#" label={$_("task")} active={state === "task"} />
        <TabElement
            href="#"
            label={$_("updates")}
            active={state === "updates"}
        />
        <div class="grow border-b-2 border-border" />
    </div>
{/if}
