<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    let pageContent: SolutionsPageContent;
    $: pageContent = {
        heroContent: {
            title: $_("solutions.academic.hero.title"),
            text: $_("solutions.academic.hero.text"),
            image: {
                src: "/assets/solutions/hero-academic.png",
                alt: $_("solutions.index.solutions.academic.illustration.alt"),
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/academic-popup.png",
                    alt: $_(
                        "solutions.academic.features.feature-1.illustration.alt"
                    ),
                },
                title: $_("solutions.academic.features.feature-1.title"),
                text: $_("solutions.academic.features.feature-1.text"),
            },
            {
                image: {
                    position: "left",
                    src: "/assets/solutions/academic-subtask.png",
                    alt: $_(
                        "solutions.academic.features.feature-2.illustration.alt"
                    ),
                },
                title: $_("solutions.academic.features.feature-2.title"),
                text: $_("solutions.academic.features.feature-2.text"),
            },
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/academic-update.png",
                    alt: $_(
                        "solutions.academic.features.feature-3.illustration.alt"
                    ),
                },
                title: $_("solutions.academic.features.feature-3.title"),
                text: $_("solutions.academic.features.feature-3.text"),
            },
        ],
    };
</script>

<SolutionsPage {pageContent} />
