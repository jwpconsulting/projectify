<script lang="ts">
    import CheckBox from "$lib/figma/CheckBox.svelte";

    import { falseTrue, trueFalse, fr, fc } from "$lib/storybook";
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
