<script lang="ts">
    import colorStyleVars from "daisyui/colors/colorNames.js";
    import hex2hsl from "daisyui/colors/hex2hsl.js";
    import { onMount } from "svelte";

    const light = {
        "primary": "#288CFF" /* Primary color */,
        "primary-focus": "#0077FF" /* Primary color - focused */,
        "primary-content":
            "#ffffff" /* Foreground content color to use on primary color */,

        "secondary": "#BEDCFF" /* Secondary color */,
        "secondary-focus": "#76B4F9" /* Secondary color - focused */,
        "secondary-content":
            "#ffffff" /* Foreground content color to use on secondary color */,

        "accent": "#EF7D69" /* Accent color */,
        "accent-focus": "#F05F46" /* Accent color - focused */,
        "accent-content":
            "#ffffff" /* Foreground content color to use on accent color */,

        "neutral": "#ffffff" /* Neutral color */,
        "neutral-focus": "#eeeeee" /* Neutral color - focused */,
        "neutral-content":
            "#333333" /* Foreground content color to use on neutral color */,

        "base-100":
            "#ffffff" /* Base color of page, used for blank backgrounds */,
        "base-200": "#F2F8FF" /* Base color, a little darker */,
        "base-300": "#d1d5db" /* Base color, even more darker */,
        "base-content":
            "#1f2937" /* Foreground content color to use on base color */,

        "info": "#2094f3" /* Info */,
        "success": "#009485" /* Success */,
        "warning": "#ff9900" /* Warning */,
        "error": "#ff5724" /* Error */,
    };

    function getStyleFromDom() {
        const styles = getComputedStyle(document.documentElement);

        const theme = {};
        const node = document.createElement("div");
        Object.entries(colorStyleVars).forEach(([key, val]) => {
            let value = styles.getPropertyValue(val as string);
            value = rgb2hex(value);
            node.style.setProperty("color", `hsla(${value})`);
            theme[key] = node.style.getPropertyValue("color");
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

    let lightArray = themeToArray(light);

    console.log(colorStyleVars);

    function dumpTheme(themeArray) {
        const th = arrayToTheme(themeArray);
        const thStr = JSON.stringify(th, null, 4);
        console.log(thStr);
        navigator.clipboard.writeText(thStr);

        console.log(getStyleFor(themeArray));
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
        const theme = getStyleFromDom();

        lightArray = themeToArray(theme);
        console.log(theme);
        console.log(lightArray);
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
