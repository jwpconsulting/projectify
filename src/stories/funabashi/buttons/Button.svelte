<script lang="ts">
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import type {
        ButtonAction,
        ButtonStyle,
        ButtonColor,
    } from "$lib/funabashi/types";
    import { buttonSizes } from "$lib/funabashi/types";

    export let label: string;
    export let style: ButtonStyle;
    export let color: ButtonColor;
    export let action: ButtonAction;
</script>

<div class="flex flex-col flex-wrap gap-2">
    {#each buttonSizes as size}
        <Button {label} {style} {color} {size} {action} />
    {/each}
</div>
