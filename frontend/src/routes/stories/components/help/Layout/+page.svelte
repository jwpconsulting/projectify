<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import Layout from "$lib/components/help/Layout.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    const heroContent: SolutionsHeroContent = {
        title: "Sample Help Page",
    };

    const content = `
# Sample Help Content

This is a sample help document.

## Section 1

This is the content of section 1.

## Section 2

This is the content of section 2.
`;
</script>

<Layout {heroContent} {content} />
