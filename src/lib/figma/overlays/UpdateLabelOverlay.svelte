<script lang="ts">
    import type { LabelSearchModule } from "$lib/types/stores";

    import FilterLabelMenu from "$lib/figma/composites/FilterLabelMenu.svelte";

    export let labelSearchModule: LabelSearchModule;
</script>

<FilterLabelMenu {labelSearchModule} canEdit={false} />
