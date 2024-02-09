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

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";

    import { page } from "$app/stores";

    $: errorMessage = $page.error?.message ?? $_("dashboard.error.title");
</script>

<div class="flex flex-col gap-6 p-16">
    <header class="flex flex-col gap-4">
        <h1 class="text-3xl font-bold">
            {errorMessage}
        </h1>
    </header>
    <main class="flex flex-col gap-4">
        <p>
            {$_("dashboard.error.description")}
        </p>
        <code>
            {errorMessage}
        </code>
        <p>
            {$_("dashboard.error.what-to-do.message")}
        </p>
        <ol class="list-inside list-disc">
            <li>
                <Anchor
                    href="/help"
                    label={$_("dashboard.error.what-to-do.options.help")}
                    size="normal"
                    openBlank
                />
            </li>
            <li>
                <Anchor
                    href="/contact-us"
                    label={$_("dashboard.error.what-to-do.options.contact-us")}
                    size="normal"
                    openBlank
                />
            </li>
        </ol>
    </main>
</div>
