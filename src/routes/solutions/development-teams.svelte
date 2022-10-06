<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { SolutionsPageContent } from "$lib/types/ui";
    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";

    let pageContent: SolutionsPageContent;
    $: pageContent = {
        heroContent: {
            header: $_("development-solutions.hero-header"),
            text: $_("development-solutions.hero-text"),
            image: {
                src: "/assets/solutions/hero-development.png",
                alt: "TODO",
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/dev-filter.png",
                    alt: "TODO",
                },
                header: $_("development-solutions.feature-1-header"),
                text: $_("development-solutions.feature-1-text"),
            },
            {
                image: {
                    position: "left",
                    src: "/assets/landing/notifications.png",
                    alt: "TODO",
                },
                header: $_("development-solutions.feature-2-header"),
                text: $_("development-solutions.feature-2-text"),
            },
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/dev-tasks.png",
                    alt: "TODO",
                },
                header: $_("development-solutions.feature-3-header"),
                text: $_("development-solutions.feature-3-text"),
            },
        ],
    };
</script>

<SolutionsPage {pageContent} />
