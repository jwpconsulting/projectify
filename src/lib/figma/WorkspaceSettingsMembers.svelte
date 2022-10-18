<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { Workspace, WorkspaceUser } from "$lib/types/workspace";
    import WorkspaceSettingsPage from "$lib/figma/WorkspaceSettingsPage.svelte";
    import InputField from "$lib/figma/InputField.svelte";
    import MemberSettings from "$lib/figma/MemberSettings.svelte";
    import Button from "$lib/figma/buttons/Button.svelte";
    export let workspace: Workspace;

    let workspaceUsers: WorkspaceUser[] | null;
    $: {
        workspaceUsers = workspace.workspace_users || null;
    }
    let workspaceUserSearch: string;
</script>

<WorkspaceSettingsPage {workspace} activeSetting="team-members">
    <div class="flex flex-col gap-4">
        <InputField
            style={{ kind: "search" }}
            name="workspaceUserSearch"
            bind:value={workspaceUserSearch}
            placeholder={$_("settings.search-members")}
        />
        <div class="flex flex-row justify-between">
            <Button
                label={$_("settings.filter-by-roles")}
                style={{ kind: "secondary" }}
                size="extra-small"
                disabled={false}
                color="blue"
            />
            <Button
                label={$_("settings.invite-new-members")}
                style={{ kind: "primary" }}
                size="extra-small"
                disabled={false}
                color="blue"
            />
        </div>
    </div>
    {#if workspaceUsers}
        <div class="">
            <div
                class="flex flex-row justify-between border-b border-border px-2 pb-4 text-sm font-bold text-utility"
            >
                <div>
                    {$_("settings.member-details")}
                </div>
                <div>
                    {$_("settings.role")}
                </div>
            </div>
            {#each workspaceUsers as workspaceUser}
                <MemberSettings {workspaceUser} />
            {/each}
        </div>
    {:else}
        no workspace users
    {/if}
</WorkspaceSettingsPage>
