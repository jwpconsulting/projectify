<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { SolutionsPageContent } from "$lib/types/ui";
    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";

    let pageContent: SolutionsPageContent;
    $: pageContent = {
        heroContent: {
            header: $_("remote-solutions.hero-header"),
            text: $_("remote-solutions.hero-text"),
            image: {
                src: "/assets/solutions/hero-remote.png",
                alt: "TODO",
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/remote-update.png",
                    alt: "TODO",
                },
                header: $_("remote-solutions.feature-1-header"),
                text: $_("remote-solutions.feature-1-text"),
            },
            {
                image: {
                    position: "left",
                    src: "/assets/landing/notifications.png",
                    alt: "TODO",
                },
                header: $_("remote-solutions.feature-2-header"),
                text: $_("remote-solutions.feature-2-text"),
            },
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/remote-tasks.png",
                    alt: "TODO",
                },
                header: $_("remote-solutions.feature-3-header"),
                text: $_("remote-solutions.feature-3-text"),
            },
        ],
    };
</script>

<SolutionsPage {pageContent} />
