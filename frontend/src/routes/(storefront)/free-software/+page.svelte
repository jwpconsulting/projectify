<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023-2024 JWP Consulting GK

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

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import { toMarkdown } from "$lib/utils/markdown";

    $: markdown = toMarkdown($_("free-software.content"));
</script>

<svelte:head>
    <title>{$_("free-software.title")}</title>
</svelte:head>

<HeroLayout heroBackground>
    <div slot="hero">
        <h1 class="text-3xl font-bold">{$_("free-software.hero")}</h1>
    </div>
    <div slot="content" class="prose">
        <p>{$_("free-software.header")}</p>
        <!-- make sure to add future authors here -->
        <ul>
            <li>Copyright 2021-2024 JWP Consulting GK</li>
        </ul>
        <!-- eslint-disable-next-line svelte/no-at-html-tags -->
        {@html markdown.content}
    </div>
</HeroLayout>
