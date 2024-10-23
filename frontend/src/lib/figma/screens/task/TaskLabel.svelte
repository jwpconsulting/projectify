<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { Pencil } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";

    import LabelC from "$lib/figma/buttons/Label.svelte";
    import type { Label } from "$lib/types/workspace";

    export let onInteract: ((anchor: HTMLElement) => void) | undefined =
        undefined;
    export let readonly = false;

    export let labels: readonly Label[];

    let btnRef: HTMLElement;
</script>

<div class="flex flex-row items-start">
    <div class="flex flex-row flex-wrap items-center gap-x-1 gap-y-2">
        {#each labels as label}
            <div class="shrink-0">
                <LabelC
                    label={{ kind: "label", label }}
                    action={!readonly && onInteract
                        ? onInteract.bind(null, btnRef)
                        : undefined}
                />
            </div>
        {/each}
        {#if onInteract && !readonly}
            <div class="shrink-0" bind:this={btnRef}>
                <LabelC
                    label={{ kind: "applyLabel" }}
                    action={onInteract.bind(null, btnRef)}
                />
            </div>
        {/if}
    </div>
    {#if readonly && onInteract}
        <button
            on:click|preventDefault={onInteract.bind(null, btnRef)}
            type="button"
        >
            <Icon src={Pencil} theme="outline" class="h-4 w-4" />
        </button>
    {/if}
</div>
