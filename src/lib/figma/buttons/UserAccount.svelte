<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
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
