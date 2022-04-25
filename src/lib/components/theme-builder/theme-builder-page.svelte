<script lang="ts">
    import { browser } from "$app/env";
    import { onMount } from "svelte";

    import ThemeBuilter from "./theme-builter.svelte";
    import { getThemeFromDom } from "./theme-utils";

    let lightTheme = null;
    let darkTheme = null;

    onMount(() => {
        if (browser) {
            lightTheme = getThemeFromDom();
            darkTheme = getThemeFromDom();
        }
    });
</script>

<div class="grid min-h-full grid-cols-2 justify-items-center bg-[#f0f0f0]">
    <ThemeBuilter theme={lightTheme} />
    <ThemeBuilter theme={darkTheme} swapLayout={true} />
</div>
