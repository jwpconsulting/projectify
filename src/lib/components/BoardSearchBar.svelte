<script lang="ts">
    import { _ } from "svelte-i18n";

    import SearchInput from "$lib/components/search-input.svelte";
    import { taskSearchInput } from "$lib/stores/dashboard";
</script>

<div class="flex w-[371px] flex-row gap-2.5">
    <SearchInput
        placeholder={$_("dashboard.search-task")}
        bind:searchText={$taskSearchInput}
    />
</div>
