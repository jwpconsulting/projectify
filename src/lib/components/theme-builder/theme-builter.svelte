<script lang="ts">
    import { getUserThemeFor, setUserThemeFor } from "$lib/stores/global-ui";
    import {
        factoryDarkThemeColors,
        factoryLightThemeColors,
    } from "$lib/themeColors";
    import Palette from "./palette.svelte";

    import {
        arrayToTheme,
        dumpTheme,
        getStyleFor,
        themeToArray,
    } from "./theme-utils";

    export let theme = null;
    export let swapLayout = false;

    export let isDark = false;

    let themeArray = themeToArray(theme) || [];

    function save() {
        const thm = arrayToTheme(themeArray);
        setUserThemeFor(thm, isDark);
    }

    function resetToFactory() {
        const theme = isDark
            ? factoryDarkThemeColors
            : factoryLightThemeColors;
        themeArray = themeToArray(theme);

        setUserThemeFor(null, isDark);
    }

    function revertToSaved() {
        const theme = getUserThemeFor(isDark);
        if (theme) {
            themeArray = themeToArray(theme);
        }
    }
</script>

<div class="flex h-[100vh] w-full flex-col text-[#333]">
    <div class="flex">
        <div
            class:order-2={swapLayout}
            class="flex h-fit shrink-0 flex-col gap-4 bg-[#f0f0f0] p-4"
        >
            {#each themeArray as color}
                <div
                    class="flex flex-row items-center overflow-hidden bg-[#fff] shadow-md"
                >
                    <input
                        class="aspect-square h-full shrink-0"
                        type="color"
                        bind:value={color.value}
                    />
                    <div class="flex grow flex-col p-2 text-xs uppercase">
                        <div class=" font-bold ">{color.name}</div>
                        <div class="text-[#888]">{color.value}</div>
                    </div>
                </div>
            {/each}
        </div>

        <!-- Components -->
        <div
            style={getStyleFor(themeArray)}
            class:order-1={swapLayout}
            class="items-top relative flex grow flex-wrap justify-center gap-4 bg-base-200"
        >
            <div
                class="sticky top-0 flex h-fit w-full flex-col flex-wrap items-center justify-start gap-4 p-4 "
            >
                <div
                    class="flex w-full flex-col gap-4 bg-base-100 p-8 shadow-sm"
                >
                    <button class="btn btn-primary btn-sm">Button</button>
                    <button class="btn btn-secondary btn-sm">Button</button>
                    <button class="btn btn-accent btn-sm">Button</button>

                    <hr class="border-base-300" />

                    <button class="btn btn-ghost btn-sm">Button</button>
                    <hr class="border-base-300" />
                    <button class="btn btn-link btn-sm">Button</button>

                    <hr class="border-base-300" />

                    <button class="btn btn-info btn-sm">Info</button>
                    <button class="btn btn-success btn-sm">Success</button>
                    <button class="btn btn-warning btn-sm">Warning</button>
                    <button class="btn btn-error btn-sm">Error</button>
                </div>

                <Palette />
            </div>
        </div>
    </div>

    <header
        class="sticky bottom-0 flex items-center justify-center gap-2 border-t border-base-300 bg-[#fff] p-2"
    >
        <button
            class="btn btn-outline btn-primary btn-sm"
            on:click={() => resetToFactory()}>Reset To factory</button
        >

        <button
            class="btn btn-outline btn-primary btn-sm"
            on:click={() => dumpTheme(themeArray)}>Dump theme</button
        >

        <button
            class="btn btn-outline btn-primary btn-sm"
            on:click={() => save()}>Save</button
        >

        <button
            class="btn btn-outline btn-primary btn-sm"
            on:click={() => revertToSaved()}>Revert</button
        >
    </header>
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
