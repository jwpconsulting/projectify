<script lang="ts">
    import { isDarkMode, saveDarkMode } from "$lib/stores/global-ui";
    import { _ } from "svelte-i18n";
    import SettingsField from "../dashboard/settings-field.svelte";

    const appearanceItems = [
        {
            label: $_("auto-system-preference"),
            isDarkMode: null,
        },
        {
            label: $_("light"),
            isDarkMode: false,
        },
        {
            label: $_("dark"),
            isDarkMode: true,
        },
    ];
</script>

<SettingsField label={$_("appearance")}>
    <div class="flex w-full flex-col">
        {#each appearanceItems as it, inx}
            <div class="form-control flex w-full">
                <label class="label flex w-full cursor-pointer gap-2">
                    <span class="label-text">{it.label}</span>
                    <input
                        type="radio"
                        name="app"
                        class="checked:bg-blue-500 radio radio-primary shrink-0"
                        checked={it.isDarkMode == $isDarkMode}
                        on:change={(e) => {
                            saveDarkMode(it.isDarkMode);
                        }}
                    />
                </label>
            </div>
        {/each}
    </div>
</SettingsField>
