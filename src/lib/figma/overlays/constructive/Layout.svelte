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
    export let onSubmit: (() => void) | undefined = undefined;
</script>

<div class="flex max-w-lg grow flex-col gap-10 rounded-lg bg-foreground p-8">
    <h1 class="text-center text-3xl font-bold">
        <slot name="title" />
    </h1>
    <form class="flex flex-col gap-8" on:submit|preventDefault={onSubmit}>
        <input type="submit" class="hidden" />
        {#if $$slots.message}
            <slot name="message" />
        {/if}
        {#if $$slots.form}
            <div class="flex flex-col gap-2">
                <slot name="form" />
            </div>
        {/if}
        <div class="flex flex-row justify-center">
            <slot name="buttons" />
        </div>
    </form>
</div>
