<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2024 JWP Consulting GK

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
    import { currentWorkspace } from "$lib/stores/dashboard/workspace";

    import type { PageData } from "./$types";

    export let data: PageData;

    $: workspace = $currentWorkspace.or(data.workspace);
</script>

<svelte:head>
    <title>{workspace.title}</title>
</svelte:head>

<div class="flex h-full flex-col items-center bg-background px-0 py-8 sm:px-2">
    <slot />
</div>
