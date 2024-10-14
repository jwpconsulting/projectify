<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import { getDisplayName } from "$lib/types/user";
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
    class="flex flex-row items-center justify-center gap-2 rounded-lg px-2 py-0.5 hover:bg-secondary-hover"
>
    {getDisplayName(user)}
    <AvatarVariant content={{ kind: "single", user }} size="medium" />
</button>
