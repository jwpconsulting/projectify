<script lang="ts">
    import {
        falseTrue,
        fc,
        fr,
        selectLabels,
        workspaceUserSelectionInputs,
    } from "$lib/storybook";

    import FilterLabel from "$lib/figma/select-controls/FilterLabel.svelte";
    import FilterUser from "$lib/figma/select-controls/FilterUser.svelte";
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
                {:else}
                    {label.label.name}
                {/if}
            </div>
            {#each falseTrue as checked}
                <SelectLabelCheckBox {label} {checked} />
            {/each}
        </div>
    {/each}
</div>

Filter user
<div class={fc}>
    {#each workspaceUserSelectionInputs as workspaceUserSelectionInput}
        <div class={fr}>
            {#each falseTrue as active}
                <div class="w-96">
                    <FilterUser
                        {workspaceUserSelectionInput}
                        {active}
                        count={125}
                    />
                </div>
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
