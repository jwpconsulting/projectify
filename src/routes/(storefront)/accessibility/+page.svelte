<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

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
<script lang="ts">
    import { _, json } from "svelte-i18n";

    import Hero from "$lib/components/layouts/Hero.svelte";
    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    import HeroAccessibility from "./hero-accessibility.png";

    $: heroContent = {
        title: $_("accessibility.hero.title"),
        image: {
            src: HeroAccessibility,
            alt: $_("accessibility.hero.illustration.alt"),
        },
    } satisfies SolutionsHeroContent;

    $: sections = [
        {
            title: $_("accessibility.goals.title"),
            text: $_("accessibility.goals.text"),
        },
        {
            title: $_("accessibility.measures.title"),
            list: $json("accessibility.measures.list") as string[],
        },
        {
            title: $_("accessibility.conformance.title"),
            text: $_("accessibility.conformance.text"),
        },
        {
            title: $_("accessibility.compatibility.title"),
            text: $_("accessibility.compatibility.text"),
        },
        {
            title: $_("accessibility.platform.title"),
            text: $_("accessibility.platform.text"),
        },
        {
            title: $_("accessibility.website.title"),
            list: $json("accessibility.website.list") as string[],
        },
        {
            title: $_("accessibility.limitations.title"),
            text: $_("accessibility.limitations.text"),
            list: $json("accessibility.limitations.list") as string[],
        },
        {
            title: $_("accessibility.evaluation.title"),
            text: $_("accessibility.evaluation.text"),
        },
        {
            title: $_("accessibility.contact.title"),
            text: $_("accessibility.contact.text"),
        },
    ];
</script>

<HeroLayout>
    <Hero slot="hero" {heroContent} />

    <div slot="content" class="flex flex-col gap-4">
        {#each sections as section}
            <section class="flex flex-col gap-4">
                <h2 class="pt-4 text-3xl font-bold">
                    {section.title}
                </h2>
                {#if section.text}
                    <p>
                        {section.text}
                    </p>
                {/if}
                {#if section.list}
                    <ul>
                        {#each section.list as item}
                            <li>
                                {item}
                            </li>
                        {/each}
                    </ul>
                {/if}
            </section>
        {/each}
    </div>
</HeroLayout>
