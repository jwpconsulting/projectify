<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    import HeroResearch from "../assets/hero-research.png";
    import ResearchTasks from "../assets/research-tasks.png";
    import ResearchUpdate from "../assets/research-update.png";

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
                    position: "left",
                    src: ResearchUpdate,
                    alt: $_(
                        "solutions.research.features.feature-2.illustration.alt",
                    ),
                },
                title: $_("solutions.research.features.feature-2.title"),
                text: $_("solutions.research.features.feature-2.text"),
            },
            {
                image: {
                    position: "right",
                    src: "/assets/landing/filters.png",
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
