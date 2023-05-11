<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Tag } from "@steeze-ui/heroicons";
    import type { Label } from "$lib/types/workspace";
    import LabelC from "$lib/figma/buttons/Label.svelte";

    export let action: ((anchor: HTMLElement) => void) | undefined = undefined;

    export let labels: Label[];

    let btnRef: HTMLElement;
</script>

<div class="flex flex-row items-center gap-4">
    <Icon src={Tag} class="w-6" theme="outline" />
    {#each labels as label}
        <LabelC
            label={{ kind: "label", label }}
            action={action ? action.bind(null, btnRef) : undefined}
        />
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
