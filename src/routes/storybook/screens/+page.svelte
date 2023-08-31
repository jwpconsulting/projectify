<script lang="ts">
    import { fc, workspace } from "$lib/storybook";

    import { browser } from "$app/environment";
    import ConfirmPasswordReset from "$lib/figma/screens/auth/ConfirmPasswordReset.svelte";
    import LogIn from "$lib/figma/screens/auth/LogIn.svelte";
    import RequestPasswordReset from "$lib/figma/screens/auth/RequestPasswordReset.svelte";
    import SignUp from "$lib/figma/screens/auth/SignUp.svelte";
    import WorkspaceSettingsBilling from "$lib/figma/screens/workspace-settings/WorkspaceSettingsBilling.svelte";
    import WorkspaceSettingsGeneral from "$lib/figma/screens/workspace-settings/WorkspaceSettingsGeneral.svelte";
    import WorkspaceSettingsMembers from "$lib/figma/screens/workspace-settings/WorkspaceSettingsMembers.svelte";
    import WorkspaceSettingsTabBar from "$lib/figma/screens/workspace-settings/WorkspaceSettingsTabBar.svelte";
    import { settingKinds } from "$lib/types/dashboard";
</script>

{#if browser}
    <div class={fc}>
        {#each settingKinds as activeSetting}
            <WorkspaceSettingsTabBar {workspace} {activeSetting} />
        {/each}
    </div>

    <div class={fc}>
        <WorkspaceSettingsGeneral {workspace} />
        <WorkspaceSettingsMembers {workspace} />
        <WorkspaceSettingsBilling {workspace} />
    </div>
{/if}

<div class={fc}>
    <div class="w-[500px]">
        <LogIn />
    </div>
    <div class="w-[500px]">
        <SignUp />
    </div>
    <div class="w-[500px]">
        <RequestPasswordReset />
    </div>
    <div class="w-[500px]">
        <ConfirmPasswordReset
            email="hello@example.com"
            token="asdhelloworld"
        />
    </div>
</div>
