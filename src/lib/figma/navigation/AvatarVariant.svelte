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
    import { AvatarMarble as Avatar } from "svelte-boring-avatars";

    import type {
        AvatarStateSize,
        AvatarVariantContent,
    } from "$lib/figma/types";
    import { getDisplayName } from "$lib/types/user";
    import { tw } from "$lib/utils/ui";

    export let content: AvatarVariantContent;
    export let size: AvatarStateSize;
    $: user = content.user;

    $: outerSize = {
        large: tw`h-24 w-24`,
        medium: tw`h-8 w-8`,
        small: tw`h-6 w-6`,
        hoverable: tw`h-6 w-6 group-hover:h-8 group-hover:w-8`,
    }[size];
    type Size = 24 | 32 | 92;
    let innerSize: Size;
    const sizes: Record<AvatarStateSize, Size> = {
        large: 92,
        medium: 32,
        small: 24,
        hoverable: 32,
    } as const;
    $: innerSize = sizes[size];
    $: profilePicture = user ? user.profile_picture : undefined;
    $: name = user ? `${user.email}${getDisplayName(user)}` : undefined;
</script>

<div class="p-0.5">
    <div
        class="flex {outerSize} items-center justify-center rounded-full border border-primary"
        class:bg-background={user === undefined}
    >
        {#if profilePicture}
            <img
                src={profilePicture}
                alt={name}
                class="h-full w-full overflow-x-auto rounded-full object-cover object-center"
            />
        {:else if name}
            <Avatar size={innerSize} {name} />
        {/if}
    </div>
</div>
