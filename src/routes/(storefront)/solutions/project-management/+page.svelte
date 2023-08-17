<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    let pageContent: SolutionsPageContent;
    $: pageContent = {
        heroContent: {
            header: $_("project-solutions.hero-header"),
            text: $_("project-solutions.hero-text"),
            image: {
                src: "/assets/solutions/hero-project-management.png",
                alt: "TODO",
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/project-member.png",
                    alt: "TODO",
                },
                header: $_("project-solutions.feature-1-header"),
                text: $_("project-solutions.feature-1-text"),
            },
            {
                image: {
                    position: "left",
                    src: "/assets/landing/notifications.png",
                    alt: "TODO",
                },
                header: $_("project-solutions.feature-2-header"),
                text: $_("project-solutions.feature-2-text"),
            },
            {
                image: {
                    position: "right",
                    src: "/assets/landing/filters.png",
                    alt: "TODO",
                },
                header: $_("project-solutions.feature-3-header"),
                text: $_("project-solutions.feature-3-text"),
            },
            {
                image: {
                    position: "left",
                    src: "/assets/solutions/project-permissions.png",
                    alt: "TODO",
                },
                header: $_("project-solutions.feature-4-header"),
                text: $_("project-solutions.feature-4-text"),
            },
        ],
    };
</script>

<SolutionsPage {pageContent} />
