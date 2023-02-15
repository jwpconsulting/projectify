<script lang="ts">
    import type { ButtonStyle } from "$lib/figma/types";
    import Button from "$lib/figma/buttons/Button.svelte";
    import { action } from "@storybook/addon-actions";

    import { buttonSizes, buttonColors } from "$lib/figma/types";
    import { fr, fc, falseTrue } from "$lib/storybook";

    export let style: ButtonStyle;
</script>

<div class={fr}>
    {#each buttonColors as color}
        <div class={fc}>
            {#each buttonSizes as size}
                <div class={fr}>
                    {#each falseTrue as disabled}
                        <Button
                            label="Hello, World"
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
    {/each}
</div>
