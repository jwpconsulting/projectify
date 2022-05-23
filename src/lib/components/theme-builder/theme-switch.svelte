<script lang="ts">
    import { isDarkMode, saveDarkMode } from "$lib/stores/global-ui";
    import SettingsField from "../dashboard/settings-field.svelte";

    const appearanceItems = [
        {
            label: "Auto (System preference)",
            isDarkMode: null,
        },
        {
            label: "Light",
            isDarkMode: false,
        },
        {
            label: "Dark",
            isDarkMode: true,
        },
    ];
</script>

<SettingsField label="Appearance">
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

<style lang="scss">
    .appearance-item {
        @apply flex;
    }
</style>
