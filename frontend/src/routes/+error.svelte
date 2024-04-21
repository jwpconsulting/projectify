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
    import Landing from "$lib/figma/navigation/header/Landing.svelte";
</script>

<svelte:head>
    {#if $page.status == 404}
        <title>
            {$_("error-page.404-not-found.title")}
        </title>
    {:else if $page.error}
        <title>
            {$_("error-page.other.title")}
        </title>
    {:else}
        <title>
            {$_("error-page.no-error.title")}
        </title>
    {/if}
</svelte:head>

<Landing />
<main class="flex grow flex-col gap-12 p-20">
    <header class="flex flex-col gap-12">
        <h1 class="text-5xl font-bold">
            {#if $page.status == 404}
                {$_("error-page.404-not-found.title")}
            {:else if $page.error}
                {$_("error-page.other.title")}
            {:else}
                {$_("error-page.no-error.title")}
            {/if}
        </h1>
        {#if $page.status == 404}
            <p class="text-xl font-bold">
                {$_("error-page.404-not-found.body")}
            </p>
        {:else if $page.error}
            <p>
                {$_("error-page.other.body")}
            </p>
            <p>
                {$page.error.toString()}
            </p>
        {:else}
            {$_("error-page.no-error.body")}
        {/if}
    </header>
    <section>
        <Anchor label={$_("error-page.take-me-home")} href="/" size="large" />
    </section>
</main>
