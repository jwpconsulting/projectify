<script lang="ts">
    import FilterLabelMenu from "$lib/figma/composites/FilterLabelMenu.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import type { LabelSearchModule } from "$lib/types/stores";

    export let labelSearchModule: LabelSearchModule;
</script>

<Layout>
    <FilterLabelMenu {labelSearchModule} canEdit={false} />
</Layout>
