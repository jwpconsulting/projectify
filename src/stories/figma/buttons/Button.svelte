<script lang="ts">
    import type { ButtonStyle } from "$lib/figma/types";
    import Button from "$lib/figma/buttons/Button.svelte";
    import { action } from "@storybook/addon-actions";

    import { buttonSizes, buttonColors } from "$lib/figma/types";
    import { fr, fc, falseTrue } from "$lib/storybook";
    import type { ButtonColor } from "$lib/figma/types";

    export let label: string;
    export let style: ButtonStyle;
    export let color: ButtonColor;
</script>

<div class={fc}>
    {#each buttonSizes as size}
        <div class={fr}>
            {#each falseTrue as disabled}
                <Button
                    {label}
                    {style}
                    {color}
                    {size}
                    {disabled}
                    on:click={action("This button was clicked")}
                />
            {/each}
        </div>
    {/each}
</div>
