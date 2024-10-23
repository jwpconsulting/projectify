<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<!-- @component Explain what role can do what -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/components/help/Layout.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    $: heroContent = {
        title: $_("help.roles.title"),
        text: $_("help.roles.description"),
    } satisfies SolutionsHeroContent;
</script>

<Layout {heroContent} content={$_("help.roles.content")} />
