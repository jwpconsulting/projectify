<script lang="ts">
    import FilterLabelCollapsible from "$lib/figma/FilterLabelCollapsible.svelte";

    import { setFirstWorkspace } from "$lib/stores/dashboard";
    import { browser } from "$app/env";

    if (browser) {
        setFirstWorkspace();
    }
</script>

<div class="w-96">
    <FilterLabelCollapsible />
</div>
