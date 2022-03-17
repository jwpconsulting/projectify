<script lang="ts">
    import { getColorFromInx, paletteSize } from "$lib/utils/colors";
    import { createEventDispatcher } from "svelte";

    export let selectedColorInx: number = -1;

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
            style={`--color:${color.h} ${color.s}% ${color.l}%;--color:${color.style};`}
            class:text-base-100={color.br}
            class:active={selectedColorInx % paletteSize === inx}
            class="cursor-pointer color flex shrink-0 justify-center items-center rounded-full p-2 m-2 bg-debug h-10 w-10"
            on:click={() => {
                onColorClick(inx);
            }}
        />
    {/each}
</div>

<style lang="scss">
    .color {
        --opacity: 1;
        background-color: hsla(var(--color) / var(--opacity));
        background-color: rgba(var(--color) / var(--opacity));
        border: 1px solid var(--color);
        transition: all ease-out 100ms;
        position: relative;
    }

    .color::after {
        --margin: 8px;
        content: "";
        position: absolute;
        top: var(--margin);
        left: var(--margin);
        bottom: var(--margin);
        right: var(--margin);
        background-color: #fff;
        opacity: 0.6;
        border-radius: 50%;
        transition: all ease-out 300ms;
        transform: scale(0);
    }

    .color:hover {
        --opacity: 0.5;
        transform: scale(1.1);
    }
    .color:active:not(.active) {
        --opacity: 0.3;
        transition-duration: 50ms;
        transform: scale(0.95);
    }
    .color.active {
        --opacity: 1;
        transform: scale(1);
    }
    .color.active::after {
        transform: scale(1);
    }
</style>
