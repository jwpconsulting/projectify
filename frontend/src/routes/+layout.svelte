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
    import "$lib/app.scss";
    import Footer from "$lib/figma/navigation/Footer.svelte";
    import faviconHtml from "favicon-html";

    const isDevelopment = __MODE__ === "development";
</script>

<svelte:head>
    <meta
        name="description"
        content="Projectify - Manage projects the right way"
    />
    <!-- This is statically generated, so we are good -->
    <!-- eslint-disable-next-line svelte/no-at-html-tags -->
    {@html faviconHtml}
</svelte:head>

<noscript>
    <section class="flex w-full flex-col gap-2 bg-destructive/30 p-4">
        <h1 class="text-center font-bold">
            {$_("navigation.header.noscript.body")}
        </h1>
        <p>{$_("navigation.header.noscript.personal-note")}</p>
    </section>
</noscript>

{#if isDevelopment}
    <p
        class="absolute left-0 top-0 w-full bg-destructive/30 text-center font-bold"
    >
        {$_("navigation.header.development-preview")}
    </p>
{/if}

<slot />
<Footer />
