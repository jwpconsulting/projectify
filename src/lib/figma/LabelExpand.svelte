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
</script>

<div class="flex flex-col items-center gap-6">
    <Squoval
        state="active"
        icon="label"
        on:click={toggleLabelExpandOpen}
        active={$selectedLabels.kind !== "allLabels"}
    />
    {#if $labelExpandOpen}
        <div class="flex flex-col items-center gap-2">
            {#if $currentWorkspace && $currentWorkspace.labels}
                <SelectLabelFocus
                    label={{ kind: "allLabels" }}
                    active={$selectedLabels.kind === "allLabels"}
                    on:click={() => selectLabel({ kind: "allLabels" })}
                    contained={false}
                />
                <SelectLabelFocus
                    label={{ kind: "noLabel" }}
                    active={$selectedLabels.kind === "noLabel"}
                    on:click={() => selectLabel({ kind: "noLabel" })}
                    contained={false}
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
                        contained={false}
                    />
                {/each}
            {/if}
        </div>
    {/if}
</div>
