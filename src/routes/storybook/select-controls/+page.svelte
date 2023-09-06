<script lang="ts">
    import { falseTrue, fc, fr, selectLabels } from "$lib/storybook";

    import FilterLabel from "$lib/figma/select-controls/FilterLabel.svelte";
    import SelectLabelCheckBox from "$lib/figma/select-controls/SelectLabelCheckBox.svelte";
</script>

Select label focus
<div class={fr}>
    {#each selectLabels as label}
        <div class={`${fc} items-center`}>
            <div class="capitalize">
                {#if label.kind === "allLabels"}
                    all labels
                {:else if label.kind === "noLabel"}
                    no label
                {:else if label.kind === "label"}
                    {label.label.name}
                {/if}
            </div>
            {#each falseTrue as checked}
                <SelectLabelCheckBox {label} {checked} />
            {/each}
        </div>
    {/each}
</div>

Filter label
<div class={fc}>
    {#each selectLabels as label}
        <div class={fr}>
            {#each falseTrue as checked}
                <div class="w-48">
                    <FilterLabel {label} {checked} />
                </div>
            {/each}
        </div>
    {/each}
</div>
