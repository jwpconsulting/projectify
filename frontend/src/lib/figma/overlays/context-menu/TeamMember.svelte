<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    // TODO if this is for assignment, we should call it
    // context-menu/TeamMemberAssignment ?
    // Rename consistent with the other context menus
    import FilterTeamMember from "$lib/figma/composites/FilterTeamMember.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import type { TeamMemberAssignment } from "$lib/types/stores";

    export let teamMemberAssignment: TeamMemberAssignment;
</script>

<Layout>
    <FilterTeamMember mode={{ kind: "assign", teamMemberAssignment }} />
</Layout>
