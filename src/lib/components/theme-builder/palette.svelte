<script lang="ts">
    import { getColorFromInx, paletteSize } from "$lib/utils/colors";

    let colors = Array(paletteSize)
        .fill({})
        .map((it, i) => {
            return getColorFromInx(i);
        });

    console.log(colors);
</script>

<div class="flex flex-wrap p-8">
    {#each colors as color, inx}
        <div
            style={`--color:${color.h} ${color.s}% ${color.l}%; 
             --color:${color.style};   
            `}
            class:text-base-100={color.br}
            class="color bg-debug m-2 flex h-10 w-10 items-center justify-center rounded-full p-2"
        >
            {inx}
        </div>
    {/each}
</div>

<style lang="scss">
    .color {
        --opacity: 1;
        background-color: hsla(var(--color) / var(--opacity));
        background-color: rgba(var(--color) / var(--opacity));
    }
</style>
