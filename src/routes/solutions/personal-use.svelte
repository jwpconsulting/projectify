<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { SolutionsPageContent } from "$lib/types/ui";
    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";

    let pageContent: SolutionsPageContent;
    $: pageContent = {
        heroContent: {
            header: $_("personal-solutions.hero-header"),
            text: $_("personal-solutions.hero-text"),
            image: {
                src: "/assets/solutions/hero-personal.png",
                alt: "TODO",
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/personal-tasks.png",
                    alt: "TODO",
                },
                header: $_("personal-solutions.feature-1-header"),
                text: $_("personal-solutions.feature-1-text"),
            },
            {
                image: {
                    position: "left",
                    src: "/assets/solutions/personal-subtask.png",
                    alt: "TODO",
                },
                header: $_("personal-solutions.feature-2-header"),
                text: $_("personal-solutions.feature-2-text"),
            },
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/personal-task-collab.png",
                    alt: "TODO",
                },
                header: $_("personal-solutions.feature-3-header"),
                text: $_("personal-solutions.feature-3-text"),
            },
        ],
    };
</script>

<SolutionsPage {pageContent} />
