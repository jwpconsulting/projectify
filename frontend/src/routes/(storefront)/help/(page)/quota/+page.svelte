<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<!-- @component Explain how quotas work for paid/trial workspaces -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/components/help/Layout.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    $: heroContent = {
        title: $_("help.quota.title"),
        text: $_("help.quota.description"),
    } satisfies SolutionsHeroContent;
</script>

<Layout {heroContent} content={$_("help.quota.content")} />
