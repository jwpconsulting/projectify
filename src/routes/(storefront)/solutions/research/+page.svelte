<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    let pageContent: SolutionsPageContent;
    $: pageContent = {
        heroContent: {
            title: $_("solutions.research.hero.title"),
            text: $_("solutions.research.hero.text"),
            image: {
                src: "/assets/solutions/hero-research.png",
                alt: $_("solutions.index.solutions.research.illustration.alt"),
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/research-tasks.png",
                    alt: $_(
                        "solutions.research.features.feature-1.illustration.alt"
                    ),
                },
                title: $_("solutions.research.features.feature-1.title"),
                text: $_("solutions.research.features.feature-1.text"),
            },
            {
                image: {
                    position: "left",
                    src: "/assets/solutions/research-update.png",
                    alt: $_(
                        "solutions.research.features.feature-2.illustration.alt"
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
                        "solutions.research.features.feature-3.illustration.alt"
                    ),
                },
                title: $_("solutions.research.features.feature-3.title"),
                text: $_("solutions.research.features.feature-3.text"),
            },
        ],
    };
</script>

<SolutionsPage {pageContent} />
