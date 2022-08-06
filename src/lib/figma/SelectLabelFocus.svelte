<script lang="ts">
    import SelectLabelColor from "$lib/figma/SelectLabelColor.svelte";
    import { createEventDispatcher } from "svelte";
    import type { SelectLabel } from "$lib/figma/types";

    export let label: SelectLabel;
    export let active: boolean;

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="rounded-1.5xl border border-transparent focus:border-base-content focus:outline-none"
>
    <SelectLabelColor {label} {active} contained={true} />
</button>
