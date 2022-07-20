<script lang="ts">
    import type { WorkspaceUser } from "$lib/types";
    import { selectedWorkspaceUser } from "$lib/stores/dashboard";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Check } from "@steeze-ui/heroicons";
    import WorkspaceUserAvatar from "$lib/components/WorkspaceUserAvatar.svelte";
    import { _ } from "svelte-i18n";

    export let workspaceUser: WorkspaceUser | "unassigned";
    let isSelected: boolean;

    $: {
        if (!$selectedWorkspaceUser) {
            isSelected = false;
        } else if ($selectedWorkspaceUser === "unassigned") {
            if (workspaceUser === "unassigned") {
                isSelected = true;
            } else {
                isSelected = false;
            }
        } else {
            if (workspaceUser === "unassigned") {
                isSelected = false;
            } else if ($selectedWorkspaceUser.uuid === workspaceUser.uuid) {
                isSelected = true;
            } else {
                isSelected = false;
            }
        }
    }

    function selectWorkspaceUser() {
        if (workspaceUser === "unassigned") {
            if ($selectedWorkspaceUser === "unassigned") {
                $selectedWorkspaceUser = null;
            } else {
                $selectedWorkspaceUser = "unassigned";
            }
        } else {
            if (
                $selectedWorkspaceUser === null ||
                $selectedWorkspaceUser === "unassigned"
            ) {
                $selectedWorkspaceUser = workspaceUser;
            } else if ($selectedWorkspaceUser.uuid === workspaceUser.uuid) {
                $selectedWorkspaceUser = null;
            } else {
                $selectedWorkspaceUser = workspaceUser;
            }
        }
    }
</script>

<button
    class="group flex flex-row justify-between px-5 py-2 hover:bg-base-200"
    on:click={selectWorkspaceUser}
>
    <div class="flex flex-row items-center gap-2">
        <div class="flex flex-row p-0.5">
            <div class="h-4 w-4">
                {#if isSelected}
                    <Icon
                        src={Check}
                        theme="outline"
                        class="rounded border border-secondary bg-primary text-base-100"
                    />
                {:else}
                    <Icon
                        src={Check}
                        theme="outline"
                        class="rounded border border-secondary text-base-100 group-hover:border-base-100 group-hover:bg-secondary group-hover:text-secondary"
                    />
                {/if}
            </div>
        </div>
        <div class="flex flex-row items-center gap-2">
            <div
                class="flex flex h-6 w-6 flex-row items-center justify-center"
            >
                <WorkspaceUserAvatar {workspaceUser} size={20} />
            </div>
            <div class="text-regular text-xs capitalize">
                {#if workspaceUser === "unassigned"}
                    {$_("filter-workspace-user.assigned-nobody")}
                {:else}
                    {workspaceUser.user.full_name || workspaceUser.user.email}
                {/if}
            </div>
        </div>
    </div>
</button>
