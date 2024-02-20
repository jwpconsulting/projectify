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
<!-- @component Explain how quotas work for paid/trial workspaces -->
<script lang="ts">
    import { marked } from "marked";
    import { gfmHeadingId } from "marked-gfm-heading-id";
    import { _, json } from "svelte-i18n";

    import Layout from "$lib/components/help/Layout.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    marked.use(gfmHeadingId());
    const text = marked.parse(
        `
# General
# Trial
# Paid
`,
    );
    $: heroContent = {
        title: $_("help.quota.title"),
        text: $_("help.quota.description"),
    } satisfies SolutionsHeroContent;

    $: sections = $json("help.quota.sections") as {
        id: string;
        content: string;
        title: string;
    }[];
</script>

<Layout {heroContent} {sections}>
    <div class="prose" slot="content">
        <!-- eslint-disable-next-line svelte/no-at-html-tags -->
        {@html text}
    </div>
</Layout>
