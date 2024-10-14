<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Hero from "$lib/components/layouts/Hero.svelte";
    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";
    import { helpTopics } from "$lib/utils/i18n";
    import { toMarkdown } from "$lib/utils/markdown";

    export let heroContent: SolutionsHeroContent;
    export let content: string;

    $: markdown = toMarkdown(content);

    $: helpItems = helpTopics($_);
</script>

<svelte:head>
    <title
        >{$_("help.sub-page-title", {
            values: { topic: heroContent.title },
        })}</title
    >
</svelte:head>

<HeroLayout heroBackground>
    <Hero slot="hero" {heroContent} />
    <nav slot="side" class="flex grow flex-col gap-4 sm:max-w-xs">
        <h2 class="text-3xl font-bold">{$_("help.help-sections")}</h2>
        <!-- sections -->
        <ul class="flex min-w-max list-inside list-disc flex-col gap-2">
            {#each helpItems as helpItem}
                <li><Anchor href={helpItem.href} label={helpItem.title} /></li>
            {/each}
        </ul>
    </nav>
    <div slot="content" class="prose">
        <!-- skip links -->
        <nav>
            <h3>{$_("help.skip")}</h3>
            <ul>
                {#each markdown.sections as section}
                    <li>
                        <!-- marked escapes quotes and so on as html entities -->
                        <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                        <a href={`#${section.id}`}>{@html section.title}</a>
                    </li>
                {/each}
            </ul>
        </nav>
        <!-- eslint-disable-next-line svelte/no-at-html-tags -->
        <main>{@html markdown.content}</main>
    </div>
</HeroLayout>
