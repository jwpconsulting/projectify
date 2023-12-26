<script lang="ts">
    import { Search } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import WorkspaceUserCard from "$lib/figma/screens/workspace-settings/WorkspaceUserCard.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import {
        currentWorkspaceUsers,
        currentWorkspace,
    } from "$lib/stores/dashboard";
    import { searchWorkspaceUsers } from "$lib/stores/dashboard/workspaceUserFilter";
    import { openConstructiveOverlay } from "$lib/stores/globalUi";
    import type { SearchInput } from "$lib/types/base";
    import type { WorkspaceUser } from "$lib/types/workspace";

    import type { PageData } from "./$types";

    export let data: PageData;

    $: workspace = $currentWorkspace ?? data.workspace;

    let filter: SearchInput = undefined;
    let workspaceUsers: WorkspaceUser[] = [];
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
        style={{ inputType: "text" }}
        name="workspaceUserSearch"
        bind:value={filter}
        label={$_("workspace-settings.workspace-users.search.label")}
        placeholder={$_(
            "workspace-settings.workspace-users.search.placeholder",
        )}
    >
        <Icon slot="left" src={Search} class="w-4" theme="outline" />
    </InputField>
    <Button
        action={{ kind: "button", action: inviteWorkspaceUser }}
        label={$_(
            "workspace-settings.workspace-users.invite-new-workspace-users",
        )}
        style={{ kind: "primary" }}
        size="medium"
        color="blue"
    />
</div>
<table class="grid w-full grid-cols-4 items-center gap-y-4 px-2">
    <thead class="contents">
        <tr class="contents">
            <th class="col-span-2 border-b border-border text-left font-bold"
                >{$_(
                    "workspace-settings.workspace-users.workspace-user-details",
                )}</th
            >
            <th class="border-b border-border text-left font-bold"
                >{$_("workspace-settings.workspace-users.role")}</th
            >
            <th class="border-b border-border text-left font-bold"
                >{$_("workspace-settings.workspace-users.actions.action")}</th
            >
        </tr>
    </thead>
    <tbody class="contents">
        {#each workspaceUsers as workspaceUser}
            <WorkspaceUserCard {workspaceUser} />
        {:else}
            <td class="col-span-4">
                {$_(
                    "workspace-settings.workspace-users.no-workspace-users-found",
                )}
            </td>
        {/each}
    </tbody>
</table>
