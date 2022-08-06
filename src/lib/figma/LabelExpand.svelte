<script lang="ts">
    import {
        currentWorkspace,
        selectedLabels,
        labelExpandOpen,
        toggleLabelExpandOpen,
        selectLabel,
    } from "$lib/stores/dashboard";
    import SelectLabelFocus from "$lib/figma/SelectLabelFocus.svelte";
    import Squoval from "$lib/figma/Squoval.svelte";

    let active: boolean;
    $: {
        active = $selectedLabels.kind !== "allLabels";
    }
</script>

<div class="flex flex-col items-center gap-6">
    <Squoval
        state="active"
        icon="label"
        on:click={toggleLabelExpandOpen}
        {active}
    />
    {#if $labelExpandOpen}
        <div class="flex flex-col items-center gap-2">
            {#if $currentWorkspace && $currentWorkspace.labels}
                <SelectLabelFocus
                    label={{ kind: "noLabel" }}
                    active={$selectedLabels.kind === "noLabel"}
                    on:click={() => selectLabel({ kind: "noLabel" })}
                />
                {#each $currentWorkspace.labels as label}
                    <SelectLabelFocus
                        label={{ kind: "label", label: label }}
                        active={$selectedLabels.kind === "labels"
                            ? $selectedLabels.labelUuids.has(label.uuid)
                            : false}
                        on:click={() =>
                            selectLabel({
                                kind: "label",
                                labelUuid: label.uuid,
                            })}
                    />
                {/each}
            {/if}
        </div>
    {/if}
</div>
