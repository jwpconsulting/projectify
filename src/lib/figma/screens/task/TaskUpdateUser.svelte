<script lang="ts">
    import type { WorkspaceUser } from "$lib/types/workspace";
    import UpdateUser from "$lib/figma/buttons/UpdateUser.svelte";

    // Either a user has been assigned, or if not we should ask the user
    // to assign a user
    export let workspaceUser: WorkspaceUser | null;
    export let action: ((anchor: HTMLElement) => void) | undefined = undefined;

    let btnRef: HTMLElement;
</script>

<div class="flex flex-row items-center gap-4">
    <div bind:this={btnRef}>
        <UpdateUser
            action={action ? action.bind(null, btnRef) : undefined}
            user={workspaceUser ? workspaceUser.user : null}
        />
    </div>
</div>
