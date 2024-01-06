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
    import { _ } from "svelte-i18n";

    import { page } from "$app/stores";

    $: error = $page.error ?? {
        message: "No error was found, this is unexpected!",
    };
</script>

<div class="flex flex-col gap-6 p-16">
    <header class="flex flex-col gap-4">
        <h1 class="text-3xl font-bold">
            {$_("dashboard.error.title")}

            {error.message}
        </h1>
    </header>
    <main class="flex flex-col gap-4">
        <p>
            {$_("dashboard.error.description")}
        </p>
        <code>
            {error.message}
        </code>
        <p>
            {$_("dashboard.error.what-to-do.message")}
        </p>
        <ol>
            {#each $_("dashboard.error.what-to-do.options") as option}
                <li>
                    {option}
                </li>
            {/each}
        </ol>
    </main>
</div>
