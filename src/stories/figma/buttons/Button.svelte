<script lang="ts">
    import type {
        ButtonAction,
        ButtonStyle,
        ButtonColor,
    } from "$lib/figma/types";
    import Button from "$lib/figma/buttons/Button.svelte";

    import { buttonSizes } from "$lib/figma/types";
    import { falseTrue, fc, fr } from "$lib/storybook";

    export let label: string;
    export let style: ButtonStyle;
    export let color: ButtonColor;
    export let action: ButtonAction;
</script>

<div class={fc}>
    {#each buttonSizes as size}
        <div class={fr}>
            {#each falseTrue as disabled}
                <Button {label} {style} {color} {size} {action} {disabled} />
            {/each}
        </div>
    {/each}
</div>
