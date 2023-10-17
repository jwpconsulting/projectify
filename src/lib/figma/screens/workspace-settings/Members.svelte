<script lang="ts">
    import { _ } from "svelte-i18n";

    import MemberCard from "$lib/figma/screens/workspace-settings/MemberCard.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { currentWorkspace } from "$lib/stores/dashboard";
    import type { Workspace, WorkspaceUser } from "$lib/types/workspace";

    export let workspace: Workspace;

    let workspaceUsers: WorkspaceUser[];
    $: {
        workspaceUsers = workspace.workspace_users ?? [];
    }
    let workspaceUserSearch: string;

    $: workspace = $currentWorkspace ?? workspace;
</script>

<div class="flex flex-col gap-4">
    <InputField
        style={{ kind: "search" }}
        name="workspaceUserSearch"
        bind:value={workspaceUserSearch}
        placeholder={$_("workspace-settings.members.search-members")}
    />
    <div class="flex flex-row justify-between">
        <Button
            action={{ kind: "button", action: console.error }}
            label={$_("workspace-settings.members.filter-by-roles")}
            style={{ kind: "secondary" }}
            size="extra-small"
            color="blue"
        />
        <Button
            action={{ kind: "button", action: console.error }}
            label={$_("workspace-settings.members.invite-new-members")}
            style={{ kind: "primary" }}
            size="extra-small"
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
                {$_("workspace-settings.members.member-details")}
            </div>
            <div>
                {$_("workspace-settings.members.role")}
            </div>
        </div>
        {#each workspaceUsers as workspaceUser}
            <MemberCard {workspaceUser} />
        {/each}
    </div>
{:else}
    no workspace users
{/if}
