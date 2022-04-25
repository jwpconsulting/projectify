<script lang="ts">
    import { browser } from "$app/env";
    import { onMount } from "svelte";

    import ThemeBuilter from "./theme-builter.svelte";
    import { getThemeFromDom } from "./theme-utils";

    let lightTheme = {
        "primary": "#288CFF",
        "primary-focus": "#0077FF",
        "primary-content": "#ffffff",
        "secondary": "#BEDCFF",
        "secondary-focus": "#76B4F9",
        "secondary-content": "#ffffff",
        "accent": "#EF7D69",
        "accent-focus": "#F05F46",
        "accent-content": "#ffffff",
        "neutral": "#ffffff",
        "neutral-focus": "#eeeeee",
        "neutral-content": "#333333",
        "base-100": "#ffffff",
        "base-200": "#F2F8FF",
        "base-300": "#d1d5db",
        "base-content": "#1f2937",
        "info": "#2094f3",
        "success": "#009485",
        "warning": "#ff9900",
        "error": "#ff5724",
    };

    let darkTheme = { ...lightTheme };
</script>

<div class="grid min-h-full grid-cols-2 justify-items-center bg-[#f0f0f0]">
    <ThemeBuilter theme={lightTheme} />
    <ThemeBuilter theme={darkTheme} swapLayout={true} />
</div>
