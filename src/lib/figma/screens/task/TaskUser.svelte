<script lang="ts">
    // TODO rename me to TaskWorkspaceUser
    // or, actually: leave out the Task* prefix for all fields. It's kind of
    // redundant
    import UpdateUser from "$lib/figma/buttons/UpdateUser.svelte";
    import type { WorkspaceUser } from "$lib/types/workspace";

    // Either a user has been assigned, or if not we should ask the user
    // to assign a user
    export let workspaceUser: WorkspaceUser | undefined;
    export let onInteract: ((anchor: HTMLElement) => void) | undefined =
        undefined;

    let btnRef: HTMLElement;
</script>

<div class="flex flex-row items-center gap-4" bind:this={btnRef}>
    <UpdateUser
        action={onInteract ? onInteract.bind(null, btnRef) : undefined}
        user={workspaceUser?.user ?? null}
    />
</div>
