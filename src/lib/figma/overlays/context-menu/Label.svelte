<script lang="ts">
    import FilterLabelMenu from "$lib/figma/composites/FilterLabelMenu.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import type { LabelAssignment } from "$lib/types/stores";

    export let labelAssignment: LabelAssignment;
</script>

<Layout>
    <FilterLabelMenu
        canEdit={false}
        mode={{ kind: "assign", labelAssignment }}
    />
</Layout>
