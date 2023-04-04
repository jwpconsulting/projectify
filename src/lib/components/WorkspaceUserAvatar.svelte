<script lang="ts">
    import type { WorkspaceUser } from "$lib/types/workspace";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { UserCircle, UserAdd } from "@steeze-ui/heroicons";
    import UserAvatar from "$lib/components/UserAvatar.svelte";

    export let workspaceUser: WorkspaceUser | "unassigned" | "assign";
    export let size: number;
    const style = `width: ${size}px; height: ${size}px;`;
</script>

{#if workspaceUser === "unassigned"}
    <Icon src={UserCircle} theme="outline" class="text-secondary" {style} />
{:else if workspaceUser === "assign"}
    <div
        {style}
        class="h-full w-full rounded-full border border-dashed border-primary p-1"
    >
        <Icon src={UserAdd} theme="solid" class="h-full w-full text-primary" />
    </div>
{:else}
    <div
        class="flex flex-row items-center justify-center rounded-full border border-primary"
        {style}
    >
        <UserAvatar user={workspaceUser.user} {size} />
    </div>
{/if}
