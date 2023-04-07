<script lang="ts">
    import { action } from "@storybook/addon-actions";
    import type { ButtonStyle, ButtonColor } from "$lib/figma/types";
    import Button from "$lib/figma/buttons/Button.svelte";

    import { buttonSizes } from "$lib/figma/types";
    import { falseTrue, fc, fr } from "$lib/storybook";

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
