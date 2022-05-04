<script lang="ts">
    import { isDarkMode, saveDarkMode } from "$lib/stores/global-ui";
</script>

<div class="flex gap-2">
    <div>Dark mode</div>
    <input
        type="checkbox"
        class="toggle toggle-primary toggle-md"
        checked={$isDarkMode}
        on:change={(e) => {
            saveDarkMode(e.target["checked"]);
        }}
    />
</div>
