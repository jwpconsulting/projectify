<script lang="ts">
    import WorkspaceSettingsBar from "$lib/figma/screens/WorkspaceSettingsBar.svelte";
    import MemberSettings from "$lib/figma/MemberSettings.svelte";
    import WorkspaceSettingsPage from "$lib/figma/WorkspaceSettingsPage.svelte";
    import WorkspaceSettingsGeneral from "$lib/figma/WorkspaceSettingsGeneral.svelte";
    import WorkspaceSettingsMembers from "$lib/figma/WorkspaceSettingsMembers.svelte";
    import WorkspaceSettingsBilling from "$lib/figma/screens/WorkspaceSettingsBilling.svelte";
    import LogIn from "$lib/figma/LogIn.svelte";
    import SignUp from "$lib/figma/SignUp.svelte";
    import RequestPasswordReset from "$lib/figma/RequestPasswordReset.svelte";
    import ConfirmPasswordReset from "$lib/figma/ConfirmPasswordReset.svelte";
    import { settingKinds } from "$lib/types/dashboard";

    import { fc, workspace, workspaceUser } from "$lib/storybook";

    import { browser } from "$app/env";
</script>

{#if browser}
    <div class={fc}>
        {#each settingKinds as activeSetting}
            <WorkspaceSettingsBar {workspace} {activeSetting} />
        {/each}
    </div>

    <div class="w-96">
        <MemberSettings {workspaceUser} />
    </div>

    <div class={fc}>
        <WorkspaceSettingsPage {workspace} activeSetting={settingKinds[0]} />
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
