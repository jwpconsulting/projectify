<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<!-- @component Explain how quotas work for paid/trial workspaces -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/components/help/Layout.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    $: heroContent = {
        title: $_("help.keyboard-shortcuts.title"),
        text: $_("help.keyboard-shortcuts.description"),
    } satisfies SolutionsHeroContent;
</script>

<Layout {heroContent} content={$_("help.keyboard-shortcuts.content")} />
