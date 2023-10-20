<script lang="ts">
    import { _ } from "svelte-i18n";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
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
</script>

<tr class="contents">
    <td class="col-span-3 flex flex-row items-center gap-2">
        <AvatarVariant
            content={{ kind: "multiple", users: [workspaceUser.user] }}
            size="medium"
        />
        <div class="flex flex-col gap-1">
            <div class="text-sm font-bold text-base-content">{fullName}</div>
            <div class="text-sm text-base-content">{jobTitle}</div>
        </div>
    </td>
    <td class="text-sm text-base-content">{role}</td>
</tr>
