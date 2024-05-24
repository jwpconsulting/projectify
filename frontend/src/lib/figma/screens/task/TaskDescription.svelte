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
    import { Pencil } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    export let description: string | null;
    export let readonly = false;
    export let onInteract: (() => void) | undefined = undefined;
</script>

<div class="flex w-full flex-row items-center gap-2">
    <textarea
        class="w-full rounded-lg border border-border p-2"
        rows="5"
        name="description"
        id="description"
        bind:value={description}
        placeholder={$_("task-screen.description")}
        {readonly}
    />
    {#if readonly}
        <button on:click|preventDefault={onInteract} type="button">
            <Icon src={Pencil} theme="outline" class="h-4 w-4" />
        </button>
    {/if}
</div>
