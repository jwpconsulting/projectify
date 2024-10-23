<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Hero from "$lib/components/layouts/Hero.svelte";
    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import SolutionsFeature from "$lib/components/solutions/SolutionsFeature.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    export let pageContent: SolutionsPageContent;
</script>

<svelte:head>
    <title
        >{$_("solutions.sub-page-title", {
            values: { pageTitle: pageContent.heroContent.title },
        })}</title
    >
</svelte:head>

<HeroLayout heroBackground>
    <Hero slot="hero" heroContent={pageContent.heroContent} />

    <div
        slot="content"
        class="flex w-full flex-col items-center gap-6 sm:gap-16"
    >
        {#each pageContent.features as feature}
            <SolutionsFeature {feature} />
        {/each}
    </div>
</HeroLayout>
