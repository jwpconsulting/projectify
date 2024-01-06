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
    import { Adjustments, Briefcase } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { createEventDispatcher } from "svelte";

    import type { BorderedIconType } from "$lib/figma/types";

    export let type: BorderedIconType;

    $: src = {
        workspace: Briefcase,
        filter: Adjustments,
    }[type];

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="group h-9 w-9 rounded-llg border border-transparent p-0.5 focus:border-base-content focus:outline-none"
>
    <div
        class="rounded-lg border border-border p-1 group-hover:bg-secondary-hover group-active:bg-primary group-active:text-base-100"
    >
        <Icon {src} theme="outline" />
    </div>
</button>
