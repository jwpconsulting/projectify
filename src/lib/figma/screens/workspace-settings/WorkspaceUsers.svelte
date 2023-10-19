<script lang="ts">
    // TODO can we name it workspace users instead?
    import { _ } from "svelte-i18n";

    import WorkspaceUserCard from "$lib/figma/screens/workspace-settings/WorkspaceUserCard.svelte";
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

    async function inviteWorkspaceUser() {
        await openConstructiveOverlay({
            kind: "inviteWorkspaceUser",
            workspace,
        });
    }
</script>

<div class="flex flex-col gap-4">
    <InputField
        style={{ kind: "search" }}
        name="workspaceUserSearch"
        bind:value={filter}
        label={$_("workspace-settings.workspace-users.search.label")}
        placeholder={$_(
            "workspace-settings.workspace-users.search.placeholder"
        )}
    />
    <Button
        action={{ kind: "button", action: inviteWorkspaceUser }}
        label={$_(
            "workspace-settings.workspace-users.invite-new-workspace-users"
        )}
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
            {$_("workspace-settings.workspace-users.workspace-user-details")}
        </div>
        <div>
            {$_("workspace-settings.workspace-users.role")}
        </div>
    </div>
    {#each workspaceUsers as workspaceUser}
        <WorkspaceUserCard {workspaceUser} />
    {:else}
        <p class="py-4">
            {$_("workspace-settings.workspace-users.no-workspace-users-found")}
        </p>
    {/each}
</div>
