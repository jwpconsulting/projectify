<script lang="ts">
    import SelectLabelColor from "$lib/figma/SelectLabelColor.svelte";
    import { createEventDispatcher } from "svelte";
    import type { SelectLabel } from "$lib/figma/types";

    export let label: SelectLabel;
    export let active: boolean;
    export let contained: boolean;

    $: containedStyle = contained
        ? ""
        : "focus:border-base-content focus:outline-none";

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<svelte:element
    this={contained ? "div" : "button"}
    on:click={contained ? undefined : click}
    class={`rounded-1.5xl border border-transparent ${containedStyle}`}
    class:group={!contained}
>
    <SelectLabelColor {label} {active} contained={true} />
</svelte:element>
