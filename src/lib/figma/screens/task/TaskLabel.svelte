<script lang="ts">
    import LabelC from "$lib/figma/buttons/Label.svelte";
    import type { Label } from "$lib/types/workspace";

    export let action: ((anchor: HTMLElement) => void) | undefined = undefined;

    export let labels: Label[];

    let btnRef: HTMLElement;
</script>

<div class="flex flex-row items-center">
    {#each labels as label}
        <div class="shrink-0">
            <LabelC
                label={{ kind: "label", label }}
                action={action ? action.bind(null, btnRef) : undefined}
            />
        </div>
    {/each}
    {#if action}
        <div bind:this={btnRef}>
            <LabelC
                label={{ kind: "applyLabel" }}
                action={action.bind(null, btnRef)}
            />
        </div>
    {/if}
</div>
