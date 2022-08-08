<script lang="ts">
    import type {
        WorkspaceUser,
        WorkspaceUserSelectionInput,
    } from "$lib/types";
    import {
        selectedWorkspaceUser,
        selectWorkspaceUser,
    } from "$lib/stores/dashboard";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Check } from "@steeze-ui/heroicons";
    import WorkspaceUserAvatar from "$lib/components/WorkspaceUserAvatar.svelte";
    import { _ } from "svelte-i18n";

    export let workspaceUser: WorkspaceUserSelectionInput;
    let isSelected: boolean;

    $: {
        if ($selectedWorkspaceUser.kind === workspaceUser.kind) {
            if (
                $selectedWorkspaceUser.kind === "workspaceUser" &&
                workspaceUser.kind === "workspaceUser"
            ) {
                isSelected =
                    $selectedWorkspaceUser.workspaceUserUuid ===
                    workspaceUser.workspaceUser.uuid;
            } else {
                isSelected = true;
            }
        } else {
            isSelected = false;
        }
    }

    let selection: WorkspaceUser | "unassigned" | "assign";
    $: {
        if (workspaceUser.kind === "unassigned") {
            selection = "unassigned";
        } else if (workspaceUser.kind === "allWorkspaceUsers") {
            selection = "assign";
        } else {
            selection = workspaceUser.workspaceUser;
        }
    }
</script>

<button
    class="group flex flex-row justify-between px-5 py-2 hover:bg-base-200"
    on:click={() => selectWorkspaceUser(workspaceUser)}
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
                <WorkspaceUserAvatar workspaceUser={selection} size={20} />
            </div>
            <div class="text-regular text-xs capitalize">
                {#if selection === "unassigned"}
                    {$_("filter-workspace-user.assigned-nobody")}
                {:else if selection === "assign"}
                    {$_("filter-workspace-user.assign")}
                {:else}
                    {selection.user.full_name || selection.user.email}
                {/if}
            </div>
        </div>
    </div>
</button>
