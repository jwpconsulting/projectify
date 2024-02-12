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
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";

    interface Crumb {
        href?: string;
        label: string;
    }
    export let crumbs: Crumb[];
</script>

<div class="text-sm font-bold text-utility">
    {#each crumbs as crumb, ix}
        <!-- TODO a11y make this AT compatible -->
        {#if ix > 0}
            {" "}
            &gt;
        {/if}
        {#if crumb.href}
            <Anchor label={crumb.label} size="small" href={crumb.href} />
        {:else}
            <span>{crumb.label}</span>
        {/if}
    {/each}
</div>
