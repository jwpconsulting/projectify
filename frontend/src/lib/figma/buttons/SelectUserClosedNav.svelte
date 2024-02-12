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
    import { CheckCircle } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { createEventDispatcher } from "svelte";

    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import type { AvatarVariantContent } from "$lib/figma/types";
    import type { User } from "$lib/types/user";

    export let user: User | undefined;
    export let active: boolean;

    let content: AvatarVariantContent;
    $: content = {
        kind: "single",
        user,
    };

    // TODO make select / deselect callback props instead Justus 2023-09-19
    const dispatch = createEventDispatcher();
    function click() {
        active = !active;
        if (active) {
            dispatch("select");
        } else {
            dispatch("deselect");
        }
    }
</script>

<button on:click={click} class="group relative text-primary">
    {#if active}
        <div
            class="absolute left-4 top-0 z-10 h-4 w-4 rounded-full border-2 border-base-TODO bg-primary group-hover:left-6"
        />
    {:else}
        <Icon
            src={CheckCircle}
            theme="outline"
            class="absolute left-4 top-0 z-10 h-4 w-4 rounded-full bg-base-TODO group-hover:left-6 group-active:bg-primary group-active:text-base-TODO"
        />
    {/if}
    <div class="relative z-0 p-0.5">
        <AvatarVariant {content} size="hoverable" />
    </div>
</button>
