<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { SolutionsPageContent } from "$lib/types/ui";
    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";

    let pageContent: SolutionsPageContent;
    $: pageContent = {
        heroContent: {
            header: $_("research-solutions.hero-header"),
            text: $_("research-solutions.hero-text"),
            image: {
                src: "/assets/solutions/hero-research.png",
                alt: "TODO",
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/research-tasks.png",
                    alt: "TODO",
                },
                header: $_("research-solutions.feature-1-header"),
                text: $_("research-solutions.feature-1-text"),
            },
            {
                image: {
                    position: "left",
                    src: "/assets/solutions/research-update.png",
                    alt: "TODO",
                },
                header: $_("research-solutions.feature-2-header"),
                text: $_("research-solutions.feature-2-text"),
            },
            {
                image: {
                    position: "right",
                    src: "/assets/landing/filters.png",
                    alt: "TODO",
                },
                header: $_("research-solutions.feature-3-header"),
                text: $_("research-solutions.feature-3-text"),
            },
        ],
    };
</script>

<SolutionsPage {pageContent} />
