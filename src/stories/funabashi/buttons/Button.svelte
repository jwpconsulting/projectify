<script lang="ts">
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import type {
        ButtonAction,
        ButtonStyle,
        ButtonColor,
    } from "$lib/funabashi/types";
    import { buttonSizes } from "$lib/funabashi/types";
    import { fc, fr } from "$lib/storybook";

    export let label: string;
    export let style: ButtonStyle;
    export let color: ButtonColor;
    export let action: ButtonAction;
</script>

<div class={fc}>
    {#each buttonSizes as size}
        <div class={fr}>
            <Button {label} {style} {color} {size} {action} />
        </div>
    {/each}
</div>
