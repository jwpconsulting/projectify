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
    import { Plus, X } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";

    import type { FloatingActionButtonIcon } from "$lib/figma/types";

    export let action: () => void;

    export let icon: FloatingActionButtonIcon;
    export let disabled = false;

    let iconC: typeof Plus;
    $: iconC = {
        plus: Plus,
        close: X,
    }[icon];
</script>

<button
    class="group inline rounded-llg border border-transparent p-1 focus:border-border-focus focus:outline-none"
    {disabled}
    on:click={action}
    on:keydown={action}
>
    <div
        class="rounded-lg bg-primary px-7 py-2 text-primary-content shadow-context-menu group-hover:bg-primary-hover group-active:bg-primary-pressed group-disabled:bg-disabled group-disabled:text-disabled-primary-content"
    >
        <Icon src={iconC} class="w-6" theme="outline" />
    </div>
</button>
