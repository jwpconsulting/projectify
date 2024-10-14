<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    import Filters from "../../assets/filters.png?enhanced";
    import HeroResearch from "../assets/hero-research.png?enhanced";
    import ResearchTasks from "../assets/research-tasks.png?enhanced";

    $: pageContent = {
        heroContent: {
            title: $_("solutions.research.hero.title"),
            text: $_("solutions.research.hero.text"),
            image: {
                src: HeroResearch,
                alt: $_("solutions.index.solutions.research.illustration.alt"),
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: ResearchTasks,
                    alt: $_(
                        "solutions.research.features.feature-1.illustration.alt",
                    ),
                },
                title: $_("solutions.research.features.feature-1.title"),
                text: $_("solutions.research.features.feature-1.text"),
            },
            {
                image: {
                    position: "right",
                    src: Filters,
                    alt: $_(
                        "solutions.research.features.feature-3.illustration.alt",
                    ),
                },
                title: $_("solutions.research.features.feature-3.title"),
                text: $_("solutions.research.features.feature-3.text"),
            },
        ],
    } satisfies SolutionsPageContent;
</script>

<SolutionsPage {pageContent} />
