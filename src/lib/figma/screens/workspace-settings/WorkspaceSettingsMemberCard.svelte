<script lang="ts">
    import { _ } from "svelte-i18n";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import type { WorkspaceUser } from "$lib/types/workspace";
    import { getMessageNameForRole } from "$lib/utils/i18n";

    export let workspaceUser: WorkspaceUser;

    let fullName: string;
    $: fullName = workspaceUser.user.full_name || workspaceUser.user.email;
    let jobTitle: string;
    $: jobTitle = workspaceUser.job_title || $_("settings.no-job-title");
    let role: string;
    $: role = $_(getMessageNameForRole(workspaceUser.role));
</script>

<a
    class="flex grow flex-row border border-transparent p-2 focus:border-border-focus focus:outline-none"
    href="#TODO"
>
    <div
        class="flex w-full flex-row items-center justify-between border-b border-border bg-foreground p-2 hover:bg-secondary-hover active:bg-disabled"
    >
        <div class="flex flex-row items-center gap-2">
            <AvatarVariant
                content={{ kind: "multiple", users: [workspaceUser.user] }}
                size="medium"
            />
            <div class="flex flex-col gap-1">
                <div class="text-sm font-bold text-base-content">
                    {fullName}
                </div>
                <div class="text-sm text-base-content">
                    {jobTitle}
                </div>
            </div>
        </div>
        <div class="text-sm text-base-content">
            {role}
        </div>
    </div>
</a>
