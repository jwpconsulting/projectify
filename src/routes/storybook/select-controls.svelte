<script lang="ts">
    import CheckBox from "$lib/figma/select-controls/CheckBox.svelte";
    import SelectLabelFocus from "$lib/figma/select-controls/SelectLabelFocus.svelte";
    import FilterUser from "$lib/figma/FilterUser.svelte";
    import FilterLabel from "$lib/figma/FilterLabel.svelte";

    import {
        fr,
        fc,
        trueFalse,
        falseTrue,
        selectLabels,
        workspaceUserSelectionInputs,
    } from "$lib/storybook";
</script>

Checkbox
<div class={`${fr} items-center`}>
    {#each trueFalse as disabled}
        Disabled: {disabled}
        <div class={fc}>
            {#each falseTrue as checked}
                Checked: {checked}
                <CheckBox {checked} {disabled} contained={false} />
            {/each}
        </div>
    {/each}
</div>

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
                <SelectLabelFocus {label} {checked} />
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
