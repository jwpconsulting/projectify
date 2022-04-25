<script lang="ts">
    import { browser } from "$app/env";

    import { dumpTheme, getStyleFor, themeToArray } from "./theme-utils";

    export let theme = null;
    export let swapLayout = false;

    let themeArray = theme ? themeToArray(theme) : [];
</script>

<div class="flex h-[100vh] w-full flex-col">
    <header class="flex items-center justify-center bg-[#fff] p-2">
        <button
            class="btn btn-primary btn-sm"
            on:click={() => dumpTheme(themeArray)}>Dump theme</button
        >
    </header>
    <div class="flex">
        <div
            class:order-2={swapLayout}
            class="grid-layout h-fit shrink-0 gap-4 p-4"
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
                    <div
                        class="flex grow flex-col gap-2 p-2 text-xs uppercase"
                    >
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
            class="items-top relative flex grow flex-wrap justify-center gap-4 bg-base-100"
        >
            <div
                class="sticky top-0 flex h-fit flex-wrap items-center justify-start gap-4 p-4 "
            >
                <button class="btn btn-sm">Button</button>
                <button class="btn btn-primary btn-sm">Button</button>
                <button class="btn btn-secondary btn-sm">Button</button>
                <button class="btn btn-accent btn-sm">Button</button>
                <button class="btn btn-ghost btn-sm">Button</button>
                <button class="btn btn-link btn-sm">Button</button>
                <button class="btn btn-info btn-sm">Info</button>
                <button class="btn btn-success btn-sm">Success</button>
                <button class="btn btn-warning btn-sm">Warning</button>
                <button class="btn btn-error btn-sm">Error</button>
            </div>
        </div>
    </div>
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
