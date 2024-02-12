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
    import { _ } from "svelte-i18n";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import type { AvatarVariantContent } from "$lib/figma/types";
    import { getDisplayName } from "$lib/types/user";
    import type { WorkspaceUser } from "$lib/types/workspace";

    // Either a user has been assigned, or if not we should ask the user
    // to assign a user
    export let workspaceUser: WorkspaceUser | undefined;
    export let onInteract: ((anchor: HTMLElement) => void) | undefined =
        undefined;

    let btnRef: HTMLElement;

    let avatarContent: AvatarVariantContent = {
        kind: "single",
    };
    $: {
        avatarContent = {
            kind: "single",
            user,
        };
    }

    $: user = workspaceUser?.user;

    let displayName: string | undefined = undefined;
    $: {
        displayName = user ? getDisplayName(user) : undefined;
    }

    $: action = onInteract ? onInteract.bind(null, btnRef) : undefined;
</script>

<button
    class="flex w-full flex-row items-center gap-2 rounded-2.5xl border border-dashed border-primary px-2 py-1 text-sm font-bold text-primary {action !==
    undefined
        ? 'hover:bg-background active:bg-secondary-hover'
        : ''}"
    class:bg-task-hover={user !== undefined}
    type="button"
    on:click={action}
    disabled={!action}
    bind:this={btnRef}
>
    <AvatarVariant size="small" content={avatarContent} />
    <div class="truncate">
        {#if user}
            {displayName}
        {:else if action}
            {$_("dashboard.assign-user")}
        {:else}
            {$_("dashboard.no-user-assigned")}
        {/if}
    </div>
</button>
