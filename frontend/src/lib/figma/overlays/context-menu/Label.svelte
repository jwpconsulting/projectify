<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import FilterLabelMenu from "$lib/figma/composites/FilterLabelMenu.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import type { LabelAssignment } from "$lib/types/stores";

    export let labelAssignment: LabelAssignment;
</script>

<Layout>
    <FilterLabelMenu mode={{ kind: "assign", labelAssignment }} />
</Layout>
