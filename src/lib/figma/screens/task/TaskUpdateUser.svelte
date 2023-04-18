<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { User as UserIcon } from "@steeze-ui/heroicons";
    import type { WorkspaceUser } from "$lib/types/workspace";
    import UpdateUser from "$lib/figma/buttons/UpdateUser.svelte";

    // Either a user has been assigned, or if not we should ask the user
    // to assign a user
    export let workspaceUser: WorkspaceUser | null;
    export let action: (anchor: HTMLElement) => void;

    let btnRef: HTMLElement;

    function performAction() {
        action(btnRef);
    }
</script>

<div class="flex flex-row items-center gap-4">
    <div class="w-6">
        <Icon src={UserIcon} theme="outline" />
    </div>
    <div bind:this={btnRef}>
        <UpdateUser
            action={performAction}
            user={workspaceUser ? workspaceUser.user : null}
        />
    </div>
</div>
