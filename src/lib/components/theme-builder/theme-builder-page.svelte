<script lang="ts">
    import ThemeBuilder from "./theme-builder.svelte";

    import { userTheme } from "$lib/stores/global-ui";

    import {
        factoryLightThemeColors,
        factoryDarkThemeColors,
    } from "$lib/themeColors";
    import type { ThemeColors } from "$lib/types";

    let lightTheme: ThemeColors | null = null;
    let darkTheme: ThemeColors | null = null;

    $: {
        if ($userTheme) {
            console.log("$userTheme changed ", $userTheme);

            if ($userTheme.light) {
                lightTheme = { ...$userTheme.light };
            } else {
                lightTheme = { ...factoryLightThemeColors };
            }

            if ($userTheme.dark) {
                darkTheme = { ...$userTheme.dark };
            } else {
                darkTheme = { ...factoryDarkThemeColors };
            }
        } else {
            lightTheme = { ...factoryLightThemeColors };
            darkTheme = { ...factoryDarkThemeColors };
        }
    }
</script>

<div class="grid min-h-full grid-cols-2 justify-items-center bg-[#f0f0f0]">
    <ThemeBuilder theme={lightTheme} />
    <ThemeBuilder theme={darkTheme} swapLayout={true} isDark={true} />
</div>
