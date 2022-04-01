<script lang="ts">
    import { getColorFromInx, paletteSize } from "$lib/utils/colors";
    import { createEventDispatcher } from "svelte";
    import ColorDot from "./colorDot.svelte";

    export let selectedColorInx = -1;

    const dispatch = createEventDispatcher();

    let colors = Array(paletteSize)
        .fill({})
        .map((it, i) => {
            return getColorFromInx(i);
        });

    function onColorClick(inx: number) {
        dispatch("change", { color: inx });
        selectedColorInx = inx;
    }
</script>

<div class="flex flex-wrap">
    {#each colors as color, inx}
        <div
            class="m-2 h-10 w-10 cursor-pointer"
            on:click={() => {
                onColorClick(inx);
            }}
        >
            <ColorDot
                {color}
                active={selectedColorInx % paletteSize === inx}
            />
        </div>
    {/each}
</div>
