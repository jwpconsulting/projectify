<script lang="ts">
    import { getColorFromInx } from "$lib/utils/colors";

    export let color = null;
    export let active = false;

    export let index = null;

    $: {
        if (color == null && index != null) {
            color = getColorFromInx(index);
        }
    }
</script>

<div
    style={`--color:${color.h} ${color.s}% ${color.l}%;--color:${color.style};`}
    class:text-base-100={color.br}
    class:active
    class="color flex shrink-0 justify-center items-center rounded-full p-2 w-full h-full"
/>

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
        --margin: 20%;
        content: "";
        position: absolute;
        top: var(--margin);
        left: var(--margin);
        bottom: var(--margin);
        right: var(--margin);
        background-color: #fff;
        opacity: 0.9;
        border-radius: 50%;
        transition: all ease-out 100ms;
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
