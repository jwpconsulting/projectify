<script lang="ts">
    import { isDarkMode } from "$lib/stores/global-ui";
</script>

<div class="flex gap-2">
    <div>Dark mode</div>
    <input
        type="checkbox"
        class="toggle toggle-primary toggle-md"
        bind:checked={$isDarkMode}
    />
</div>
