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
    import { ChevronDown, ChevronUp } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import type { IconSource } from "@steeze-ui/svelte-icon/types";
    import { createEventDispatcher } from "svelte";

    export let label: string;
    export let icon: IconSource;
    export let filtered: boolean;
    export let open: boolean;

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="flex w-full flex-row items-center justify-between gap-2 px-4 py-2 text-utility hover:text-base-content"
>
    <div class="flex flex-row items-center gap-4">
        <div class="flex flex-row items-center gap-2">
            <Icon src={icon} theme="outline" class="h-5 w-5" />
            <div class="font-bold">{label}</div>
        </div>
        {#if filtered}
            <div class="h-3 w-3 rounded-full bg-primary" />
        {/if}
    </div>
    <Icon
        src={open ? ChevronUp : ChevronDown}
        theme="outline"
        class="h-4 w-4"
    />
</button>
