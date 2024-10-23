<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Hero from "$lib/components/layouts/Hero.svelte";
    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";
    import { helpTopics as makeHelpTopics } from "$lib/utils/i18n";

    import HeroHelp from "./hero-help.png?enhanced";

    $: heroContent = {
        title: $_("help.hero.header.text"),
        text: $_("help.hero.header.subtext"),
        image: {
            src: HeroHelp,
            alt: $_("help.hero.image.alt"),
        },
    } satisfies SolutionsHeroContent;

    $: helpTopics = makeHelpTopics($_).filter((t) => t.isOverview !== true);
</script>

<svelte:head>
    <title>{$_("help.title")}</title>
</svelte:head>

<HeroLayout heroBackground>
    <Hero slot="hero" {heroContent} />
    <div slot="content" class="flex w-full flex-col gap-4">
        <div
            class="flex w-full flex-col gap-6 sm:grid sm:grid-cols-2 md:grid-cols-3"
        >
            {#each helpTopics as helpTopic}
                <section class="flex flex-col gap-2">
                    <h1 class="text-lg font-bold">
                        {helpTopic.title}
                    </h1>
                    <p>{helpTopic.description}</p>
                    <Anchor
                        href={helpTopic.href}
                        label={$_("help.go-to-section")}
                    />
                </section>
            {/each}
        </div>
    </div>
</HeroLayout>
