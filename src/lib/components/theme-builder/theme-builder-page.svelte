<script lang="ts">
    import ThemeBuilter from "./theme-builter.svelte";

    import { userTheme } from "$lib/stores/global-ui";

    import {
        factoryLightThemeColors,
        factoryDarkThemeColors,
    } from "$lib/themeColors";

    let lightTheme = null;
    let darkTheme = null;

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
                console.log("reset dark theme", darkTheme);
            }
        }
    }
</script>

<div class="grid min-h-full grid-cols-2 justify-items-center bg-[#f0f0f0]">
    <ThemeBuilter theme={lightTheme} />
    <ThemeBuilter theme={darkTheme} swapLayout={true} isDark={true} />
</div>
