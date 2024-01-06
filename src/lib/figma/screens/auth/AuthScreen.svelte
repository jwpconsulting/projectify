<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023, 2024 JWP Consulting GK

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
    export let title: string;
    export let action: () => Promise<void>;

    // TODO use undefined
    export let subTitle: string | null = null;
</script>

<form class="flex flex-col gap-12 p-3" on:submit|preventDefault={action}>
    <h1 class="text-center text-4xl font-bold">
        {title}
    </h1>
    {#if subTitle}
        <h2 class="text-center">
            {subTitle}
        </h2>
    {/if}
    <slot />
</form>
