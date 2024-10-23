<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/components/help/Layout.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    $: heroContent = {
        title: $_("help.trial.title"),
        text: $_("help.trial.description"),
    } satisfies SolutionsHeroContent;
</script>

<Layout {heroContent} content={$_("help.trial.content")} />
