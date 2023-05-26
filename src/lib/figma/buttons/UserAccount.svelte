<script lang="ts">
    import AvatarState from "$lib/figma/navigation/AvatarState.svelte";
    import type { User } from "$lib/types/user";
    import type { ContextMenuType } from "$lib/types/ui";
    import { openContextMenu } from "$lib/stores/globalUi";

    export let user: User;

    let contextMenuAnchor: HTMLElement;

    const contextMenuType: ContextMenuType = {
        kind: "profile",
    };

    function click() {
        openContextMenu(contextMenuType, contextMenuAnchor);
    }
</script>

<button
    on:click={click}
    bind:this={contextMenuAnchor}
    class="flex h-11 w-11 flex-row items-center justify-center rounded-lg border border-transparent hover:bg-secondary-hover focus:border-base-content focus:outline-none"
>
    <AvatarState {user} size="medium" />
</button>
