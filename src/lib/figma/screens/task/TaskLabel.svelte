<script lang="ts">
    import LabelC from "$lib/figma/buttons/Label.svelte";
    import type { Label } from "$lib/types/workspace";

    export let onInteract: ((anchor: HTMLElement) => void) | undefined =
        undefined;
    export let readonly = false;

    export let labels: Label[];

    let btnRef: HTMLElement;
</script>

<div class="flex flex-row flex-wrap items-center gap-y-2">
    {#each labels as label}
        <div class="shrink-0">
            <LabelC
                label={{ kind: "label", label }}
                action={onInteract ? onInteract.bind(null, btnRef) : undefined}
            />
        </div>
    {/each}
    {#if !readonly && onInteract}
        <div class="shrink-0" bind:this={btnRef}>
            <LabelC
                label={{ kind: "applyLabel" }}
                action={onInteract.bind(null, btnRef)}
            />
        </div>
    {/if}
</div>
