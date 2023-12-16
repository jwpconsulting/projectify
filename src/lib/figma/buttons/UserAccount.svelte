<script lang="ts">
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type { User } from "$lib/types/user";

    import AvatarVariant from "../navigation/AvatarVariant.svelte";

    export let user: User;

    let contextMenuAnchor: HTMLElement;

    const contextMenuType: ContextMenuType = {
        kind: "profile",
    };

    async function click() {
        await openContextMenu(contextMenuType, contextMenuAnchor);
    }
</script>

<button
    on:click={click}
    bind:this={contextMenuAnchor}
    class="flex h-11 w-11 flex-row items-center justify-center rounded-lg border border-transparent hover:bg-secondary-hover focus:border-base-content focus:outline-none"
>
    <AvatarVariant content={{ kind: "single", user }} size="medium" />
</button>
