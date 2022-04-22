<script lang="ts">
    import { browser } from "$app/env";

    import colorStyleVars from "daisyui/colors/colorNames.js";
    import hex2hsl from "daisyui/colors/hex2hsl.js";
    import { onMount } from "svelte";

    function getStyleFromDom() {
        const styles = getComputedStyle(document.documentElement);

        const theme = {};
        const node = document.createElement("div");
        Object.entries(colorStyleVars).forEach(([key, val]) => {
            let value = styles.getPropertyValue(val as string);
            node.style.setProperty("color", `hsla(${value})`);
            value = node.style.getPropertyValue("color");
            value = rgb2hex(value);
            theme[key] = value;
        });

        return theme;
    }

    function rgb2hex(rgb) {
        rgb = rgb.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/);
        function hex(x) {
            return ("0" + parseInt(x).toString(16)).slice(-2);
        }

        return "#" + hex(rgb[1]) + hex(rgb[2]) + hex(rgb[3]);
    }

    function themeToArray(theme) {
        return Object.entries(theme).map(([key, val]) => {
            return {
                name: key,
                value: val,
            };
        });
    }

    function arrayToTheme(arr) {
        return arr.reduce((acc, cur) => {
            acc[cur.name] = cur.value;
            return acc;
        }, {});
    }

    let lightArray = [];

    function dumpTheme(themeArray) {
        const th = arrayToTheme(themeArray);
        const thStr = JSON.stringify(th, null, 4);
        console.log(thStr);
        navigator.clipboard.writeText(thStr);
    }

    function getStyleFor(themeArray) {
        const stylesVars = themeArray.map(({ name, value }) => {
            const varName = colorStyleVars[name];
            const hsv = hex2hsl(value);
            return `${varName}: ${hsv};`;
        });

        return stylesVars.join("");
    }

    onMount(() => {
        if (browser) {
            const theme = getStyleFromDom();

            lightArray = themeToArray(theme);
            console.log(theme);
            console.log(lightArray);
        }
    });
</script>

<div class="grid min-h-full grid-cols-2 justify-items-center bg-[#f0f0f0] p-8">
    {#each ["light", "dark"] as theme}
        <div style={getStyleFor(lightArray)} class="grid-layout gap-4">
            <button
                class="btn btn-primary"
                on:click={() => dumpTheme(lightArray)}>Dump theme</button
            >
            {#each lightArray as color}
                <div
                    class="flex flex-row items-center overflow-hidden bg-[#fff] shadow-md"
                >
                    <input
                        class="aspect-square h-full shrink-0"
                        type="color"
                        bind:value={color.value}
                    />
                    <div
                        class="flex grow flex-col gap-2 p-2 text-xs uppercase"
                    >
                        <div class=" font-bold ">{color.name}</div>
                        <div class="text-[#888]">{color.value}</div>
                    </div>
                </div>
            {/each}
        </div>
    {/each}
</div>

<style lang="scss">
    .grid-layout {
        @apply grid grid-flow-row-dense;
        // grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    }

    input[type="color"] {
        -webkit-appearance: none;
        border: none;
        overflow: hidden;
    }
    input[type="color"]::-webkit-color-swatch-wrapper {
        padding: 0;
    }
    input[type="color"]::-webkit-color-swatch {
        border: none;
    }
</style>
