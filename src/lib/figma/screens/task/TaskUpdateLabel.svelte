<script lang="ts">
    import { _ } from "svelte-i18n";

    import LabelC from "$lib/figma/buttons/Label.svelte";
    import type { Label } from "$lib/types/workspace";

    export let action: ((anchor: HTMLElement) => void) | undefined = undefined;

    export let labels: Label[];

    let btnRef: HTMLElement;
</script>

<div class="flex flex-row items-center gap-4">
    {#each labels as label}
        <LabelC
            label={{ kind: "label", label }}
            action={action ? action.bind(null, btnRef) : undefined}
        />
    {:else}
        {$_("task-screen.no-labels")}
    {/each}
    {#if action}
        <div bind:this={btnRef}>
            <LabelC
                label={{ kind: "applyLabel" }}
                action={action ? action.bind(null, btnRef) : undefined}
            />
        </div>
    {/if}
</div>
