<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<!--
With no overflow, we needed to change h-screen -> min-h-screen,
otherwise the footer will be placed inside the dashboard.
TODO evaluate whether grow is still necessary. Seems that with grow set, we
wouldn't need min-h-screen, really.
-->
<script lang="ts">
    import { derived } from "svelte/store";
    import ConnectionStatus from "$lib/components/ConnectionStatus.svelte";
    import ContextMenuContainer from "$lib/components/ContextMenuContainer.svelte";
    import OverlayContainer from "$lib/components/OverlayContainer.svelte";
    import Footer from "$lib/figma/navigation/Footer.svelte";
    import HeaderDashboard from "$lib/figma/navigation/header/Dashboard.svelte";
    import SideNav from "$lib/figma/navigation/SideNav.svelte";
    import ConstructiveOverlay from "$lib/figma/overlays/constructive/ConstructiveOverlay.svelte";
    import DestructiveOverlay from "$lib/figma/overlays/DestructiveOverlay.svelte";
    import MobileMenuOverlay from "$lib/figma/overlays/MobileMenuOverlay.svelte";
    import { setContext } from "svelte";

    import { can, type Resource, type Verb } from "$lib/rules/workspace";
    import {
        mobileMenuState,
        resolveConstructiveOverlay,
        constructiveOverlayState,
        destructiveOverlayState,
        rejectDestructiveOverlay,
        rejectConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { PageData } from "./dashboard/$types";
    import { currentWorkspace } from "$lib/stores/dashboard/workspace";
    import {
        type CurrentTeamMember,
        type CurrentTeamMemberCan,
    } from "$lib/stores/dashboard/teamMember";
    import type { WorkspaceDetailTeamMember } from "$lib/types/workspace";
    import { createWsStore } from "$lib/stores/wsSubscription";
    import { getProject } from "$lib/stores/dashboard/project";

    export let data: PageData;
    const { user } = data;

    const currentProject = createWsStore("project", getProject);
    setContext("currentProject", currentProject);

    /**
     * Find current team member belonging to logged in user
     */
    const currentTeamMember: CurrentTeamMember = derived<
        [typeof currentWorkspace, typeof currentProject],
        WorkspaceDetailTeamMember | undefined
    >(
        [currentWorkspace, currentProject],
        ([$currentWorkspace, $currentProject], set) => {
            const teamMembers =
                $currentWorkspace.value?.team_members ??
                $currentProject.value?.workspace.team_members;
            if (teamMembers === undefined) {
                set(undefined);
                return;
            }
            const wsUser = teamMembers.find(
                (wsUser) => wsUser.user.email === user.email,
            );
            if (wsUser === undefined) {
                throw new Error("Couldn't find currentTeamMember");
            }
            set(wsUser);
        },
        undefined,
    );

    /**
     * A store that returns a function that allows permission checking for the
     * currently active, logged in user's team member.
     */
    const currentTeamMemberCan: CurrentTeamMemberCan = derived<
        [
            typeof currentTeamMember,
            typeof currentWorkspace,
            typeof currentProject,
        ],
        (verb: Verb, resource: Resource) => boolean
    >(
        [currentTeamMember, currentWorkspace, currentProject],
        ([$currentTeamMember, $currentWorkspace, $currentProject], set) => {
            if ($currentTeamMember === undefined) {
                console.warn("teamMember was undefined");
                set(() => false);
                return;
            }
            const quota =
                $currentWorkspace.value?.quota ??
                $currentProject.value?.workspace.quota;
            if (quota === undefined) {
                console.warn("no quota found");
                set(() => false);
                return;
            }
            const fn = (verb: Verb, resource: Resource) =>
                can(verb, resource, $currentTeamMember, quota);
            set(fn);
        },
        () => false,
    );
    setContext<CurrentTeamMember>("currentTeamMember", currentTeamMember);
    setContext<CurrentTeamMemberCan>(
        "currentTeamMemberCan",
        currentTeamMemberCan,
    );
</script>

<div class="flex min-h-screen grow flex-col">
    <HeaderDashboard {user} />
    {#if $mobileMenuState.kind === "visible"}
        <MobileMenuOverlay target={$mobileMenuState.target} />
    {/if}
    <div class="flex min-h-0 shrink grow flex-row">
        <!-- this breakpoint is in tune with the mobile menu breakpoint -->
        <div class="hidden h-full shrink-0 md:block">
            <SideNav />
        </div>
        <!-- not inserting min-w-0 will mean that this div will extend as much as
    needed around whatever is inside the slot -->
        <div class="min-w-0 grow" role="presentation">
            <slot />
        </div>
    </div>
</div>

<ConnectionStatus />

<OverlayContainer
    closeOverlay={rejectDestructiveOverlay}
    store={destructiveOverlayState}
    let:target
>
    <DestructiveOverlay {target} />
</OverlayContainer>

<OverlayContainer
    closeOverlay={rejectConstructiveOverlay}
    store={constructiveOverlayState}
    let:target
>
    <ConstructiveOverlay {target} on:cancel={resolveConstructiveOverlay} />
</OverlayContainer>

<ContextMenuContainer />

<Footer {user} />
