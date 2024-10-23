<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Hero from "$lib/components/layouts/Hero.svelte";
    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    $: heroContent = {
        title: $_("contact-us.hero-title"),
    } satisfies SolutionsHeroContent;
</script>

<svelte:head>
    <title>{$_("contact-us.title")}</title>
</svelte:head>

<HeroLayout heroBackground>
    <Hero {heroContent} slot="hero" />
    <div
        slot="content"
        class="flex flex-row items-center justify-center gap-8"
    >
        <div class="flex max-w-xl flex-col gap-4">
            <h2 class="text-lg font-bold">
                {$_("contact-us.body.title")}
            </h2>
            <p>{$_("contact-us.body.text")}</p>
            <p>
                <Anchor
                    href={$_("contact-us.email.href")}
                    label={$_("contact-us.email.label")}
                />
            </p>
        </div>
        <div class="hidden shrink basis-1/4 md:block">
            <enhanced:img
                src="./illustration.png"
                alt={$_("contact-us.illustration.alt")}
            />
        </div>
    </div>
</HeroLayout>
