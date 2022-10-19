<script lang="ts">
    import type { WorkspaceUserSelectionInput } from "$lib/types/ui";
    import AvatarV3 from "$lib/figma/navigation/AvatarV3.svelte";
    import AvatarV5 from "$lib/figma/navigation/AvatarV5.svelte";
    import CheckBox from "$lib/figma/select-controls/CheckBox.svelte";
    import { _ } from "svelte-i18n";
    import { createEventDispatcher } from "svelte";

    export let workspaceUserSelectionInput: WorkspaceUserSelectionInput;
    export let active: boolean;
    export let count: number | null;

    const dispatch = createEventDispatcher();
    function click() {
        active = !active;
        if (active) {
            dispatch("select");
        } else {
            dispatch("deselect");
        }
    }
</script>

<button
    class="group flex w-full flex-row justify-between px-5 py-2 hover:bg-background"
    on:click={click}
>
    <div class="flex flex-row items-center gap-2">
        <CheckBox bind:checked={active} disabled={false} contained={true} />
        <div class="flex flex-row items-center justify-center gap-2">
            {#if workspaceUserSelectionInput.kind === "workspaceUser"}
                <AvatarV5
                    content={{
                        kind: "multiple",
                        users: [
                            workspaceUserSelectionInput.workspaceUser.user,
                        ],
                    }}
                    size="small"
                />
            {:else}
                <AvatarV3 size="small" user={null} />
            {/if}
            <div class="text-regular text-xs capitalize">
                {#if workspaceUserSelectionInput.kind === "unassigned"}
                    {$_("filter-workspace-user.assigned-nobody")}
                {:else if workspaceUserSelectionInput.kind === "allWorkspaceUsers"}
                    {$_("filter-workspace-user.all-users")}
                {:else}
                    {workspaceUserSelectionInput.workspaceUser.user
                        .full_name ||
                        workspaceUserSelectionInput.workspaceUser.user.email}
                {/if}
            </div>
        </div>
    </div>
    {#if count}
        <div
            class="flex flex-row items-center gap-2 rounded-2.5xl border-2 border-primary bg-foreground px-2 py-1 text-xs font-bold text-primary group-hover:visible"
            class:invisible={!active}
        >
            {count}
        </div>
    {/if}
</button>
