<script lang="ts">
    import { X } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { deleteWorkspaceUser } from "$lib/repository/workspace/workspace_user";
    import { openDestructiveOverlay } from "$lib/stores/globalUi";
    import type { WorkspaceUser } from "$lib/types/workspace";
    import { getMessageNameForRole } from "$lib/utils/i18n";

    export let workspaceUser: WorkspaceUser;

    let fullName: string;
    $: fullName = workspaceUser.user.full_name ?? workspaceUser.user.email;
    let jobTitle: string;
    $: jobTitle =
        workspaceUser.job_title ??
        $_("workspace-settings.workspace-users.no-job-title");
    let role: string;
    $: role = getMessageNameForRole($_, workspaceUser.role);

    async function removeUser() {
        await openDestructiveOverlay({
            kind: "deleteWorkspaceUser",
            workspaceUser,
        });
        // TODO: Do something with the result
        await deleteWorkspaceUser(workspaceUser, { fetch });
    }
</script>

<tr class="contents">
    <td class="col-span-2 flex flex-row items-center gap-2">
        <AvatarVariant
            content={{ kind: "multiple", users: [workspaceUser.user] }}
            size="medium"
        />
        <div class="flex flex-col gap-1">
            <div class="text-sm font-bold text-base-content">{fullName}</div>
            <div class="text-sm text-base-content">{jobTitle}</div>
        </div>
    </td>
    <td class="text-left text-base-content">{role}</td>
    <td class=""
        ><Button
            label={$_("workspace-settings.workspace-users.actions.remove")}
            action={{ kind: "button", action: removeUser }}
            style={{ kind: "tertiary", icon: { position: "left", icon: X } }}
            color="red"
            size="medium"
        /></td
    >
</tr>
