<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    let pageContent: SolutionsPageContent;
    $: pageContent = {
        heroContent: {
            title: $_("solutions.development.hero.title"),
            text: $_("solutions.development.hero.text"),
            image: {
                src: "/assets/solutions/hero-development.png",
                alt: $_(
                    "solutions.index.solutions.development.illustration.alt"
                ),
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/dev-filter.png",
                    alt: $_(
                        "solutions.development.features.feature-1.illustration.alt"
                    ),
                },
                title: $_("solutions.development.features.feature-1.title"),
                text: $_("solutions.development.features.feature-1.text"),
            },
            {
                image: {
                    position: "left",
                    src: "/assets/landing/notifications.png",
                    alt: $_(
                        "solutions.development.features.feature-2.illustration.alt"
                    ),
                },
                title: $_("solutions.development.features.feature-2.title"),
                text: $_("solutions.development.features.feature-2.text"),
            },
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/dev-tasks.png",
                    alt: $_(
                        "solutions.development.features.feature-3.illustration.alt"
                    ),
                },
                title: $_("solutions.development.features.feature-3.title"),
                text: $_("solutions.development.features.feature-3.text"),
            },
        ],
    };
</script>

<SolutionsPage {pageContent} />
