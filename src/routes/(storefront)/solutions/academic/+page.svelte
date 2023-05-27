<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { SolutionsPageContent } from "$lib/types/ui";
    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";

    let pageContent: SolutionsPageContent;
    $: pageContent = {
        heroContent: {
            header: $_("academic-solutions.hero-header"),
            text: $_("academic-solutions.hero-text"),
            image: {
                src: "/assets/solutions/hero-academic.png",
                alt: "TODO",
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/academic-popup.png",
                    alt: "TODO",
                },
                header: $_("academic-solutions.feature-1-header"),
                text: $_("academic-solutions.feature-1-text"),
            },
            {
                image: {
                    position: "left",
                    src: "/assets/solutions/academic-subtask.png",
                    alt: "TODO",
                },
                header: $_("academic-solutions.feature-2-header"),
                text: $_("academic-solutions.feature-2-text"),
            },
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/academic-update.png",
                    alt: "TODO",
                },
                header: $_("academic-solutions.feature-3-header"),
                text: $_("academic-solutions.feature-3-text"),
            },
        ],
    };
</script>

<SolutionsPage {pageContent} />
