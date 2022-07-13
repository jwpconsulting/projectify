<script lang="ts">
    import {
        getColorFromInxWithPalette,
        paletteSize,
        paletteVals,
    } from "$lib/utils/colors";

    let cosPalette = [...paletteVals];

    let colors: Array<any>;
    setColors();

    function setColors() {
        colors = Array(paletteSize)
            .fill({})
            .map((_, i) => {
                return getColorFromInxWithPalette(i, cosPalette);
            });
    }
    function copyPalette(_event: Event) {
        const pStr = JSON.stringify(cosPalette, null, 4);
        navigator.clipboard.writeText(pStr);
        console.log(pStr);
    }
    const classRanges = [1, 1, 4, 4];
    function onInput(cosClass: number[], vInx: number, event: Event) {
        if (!event.target) {
            throw new Error("Expected event.target");
        }
        cosClass[vInx] = event.target["value"] / 100.0;
        setColors();
    }
</script>

<div class="flex flex-wrap p-8">
    {#each colors as color, inx}
        <div
            style={`--color:${color.h} ${color.s}% ${color.l}%; 
             --color:${color.style};
             --text-color: ${color.br ? "white" : "black"};}};   
            `}
            class="color bg-debug m-2 flex h-10 w-10 items-center justify-center rounded-full p-2"
        >
            {inx}
        </div>
    {/each}

    <div class="grid grid-cols-3 gap-4 p-4">
        {#each cosPalette as cosClass, cInx}
            {#each cosClass as cosVal, vInx}
                <div>
                    <input
                        type="range"
                        min={classRanges[cInx] * -100}
                        max={classRanges[cInx] * 100}
                        value={cosVal * 100}
                        on:input={(e) => onInput(cosClass, vInx, e)}
                        class="range"
                    />
                </div>
            {/each}
        {/each}
    </div>

    <div class="flex grow items-center justify-center p-4">
        <button class="btn btn-primary" on:click={copyPalette}>Copy</button>
    </div>
</div>

<style lang="scss">
    .color {
        --opacity: 1;
        color: var(--text-color);
        background-color: hsla(var(--color) / var(--opacity));
        background-color: rgba(var(--color) / var(--opacity));
    }
</style>
