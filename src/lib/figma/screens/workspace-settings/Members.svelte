<script lang="ts">
    // TODO can we name it workspace users instead?
    import { _ } from "svelte-i18n";

    import MemberCard from "$lib/figma/screens/workspace-settings/MemberCard.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { currentWorkspaceUsers } from "$lib/stores/dashboard";
    import { searchWorkspaceUsers } from "$lib/stores/dashboard/workspaceUserFilter";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type { SearchInput } from "$lib/types/base";
    import type { Workspace, WorkspaceUser } from "$lib/types/workspace";

    export let workspace: Workspace;
    let filter: SearchInput = undefined;
    let workspaceUsers: WorkspaceUser[];
    $: workspaceUsers = searchWorkspaceUsers($currentWorkspaceUsers, filter);

    async function inviteMember() {
        await openConstructiveOverlay({
            kind: "inviteTeamMembers",
            workspace,
        });
    }
</script>

<div class="flex flex-col gap-4">
    <InputField
        style={{ kind: "search" }}
        name="workspaceUserSearch"
        bind:value={filter}
        label={$_("workspace-settings.members.search.label")}
        placeholder={$_("workspace-settings.members.search.placeholder")}
    />
    <Button
        action={{ kind: "button", action: inviteMember }}
        label={$_("workspace-settings.members.invite-new-members")}
        style={{ kind: "primary" }}
        size="medium"
        color="blue"
    />
</div>
<!-- TODO plz make me a table -->
<div>
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
    {:else}
        <p class="py-4">
            {$_("workspace-settings.members.no-members-found")}
        </p>
    {/each}
</div>
