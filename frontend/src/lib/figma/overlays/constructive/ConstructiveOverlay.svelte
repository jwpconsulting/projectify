<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import CreateProject from "$lib/figma/overlays/constructive/CreateProject.svelte";
    import CreateSection from "$lib/figma/overlays/constructive/CreateSection.svelte";
    import RecoverProject from "$lib/figma/overlays/constructive/RecoverProject.svelte";
    import UpdateProject from "$lib/figma/overlays/constructive/UpdateProject.svelte";
    import type { ConstructiveOverlayType } from "$lib/types/ui";

    import UpdateSection from "./UpdateSection.svelte";

    export let target: ConstructiveOverlayType;
</script>

{#if target.kind === "updateProject"}
    <UpdateProject project={target.project} />
{:else if target.kind === "createProject"}
    <CreateProject workspace={target.workspace} />
{:else if target.kind === "createSection"}
    <CreateSection project={target.project} />
{:else if target.kind === "updateSection"}
    <UpdateSection section={target.section} />
{:else if target.kind === "recoverProject"}
    <RecoverProject project={target.project} />
{/if}
