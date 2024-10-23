<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import Label from "$lib/figma/overlays/context-menu/Label.svelte";
    import Profile from "$lib/figma/overlays/context-menu/Profile.svelte";
    import Project from "$lib/figma/overlays/context-menu/Project.svelte";
    import Section from "$lib/figma/overlays/context-menu/Section.svelte";
    import SideNav from "$lib/figma/overlays/context-menu/SideNav.svelte";
    import Task from "$lib/figma/overlays/context-menu/Task.svelte";
    import TeamMember from "$lib/figma/overlays/context-menu/TeamMember.svelte";
    import Workspace from "$lib/figma/overlays/context-menu/Workspace.svelte";
    import type { ContextMenuType } from "$lib/types/ui";

    export let target: ContextMenuType;
</script>

{#if target.kind === "profile"}
    <Profile />
{:else if target.kind === "workspace"}
    <Workspace workspaces={target.workspaces} />
{:else if target.kind === "sideNav"}
    <SideNav workspace={target.workspace} />
{:else if target.kind === "project"}
    <Project workspace={target.workspace} project={target.project} />
{:else if target.kind === "section"}
    <Section project={target.project} section={target.section} />
{:else if target.kind === "task"}
    <Task kind={target} />
{:else if target.kind === "updateTeamMember"}
    <TeamMember teamMemberAssignment={target.teamMemberAssignment} />
{:else if target.kind === "updateLabel"}
    <Label labelAssignment={target.labelAssignment} />
{/if}
