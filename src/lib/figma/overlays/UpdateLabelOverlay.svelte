<script lang="ts">
    import FilterLabelMenu from "$lib/figma/composites/FilterLabelMenu.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import type { LabelAssignment } from "$lib/types/stores";

    export let labelSearchModule: LabelAssignment;
</script>

<Layout>
    <FilterLabelMenu {labelSearchModule} canEdit={false} />
</Layout>
