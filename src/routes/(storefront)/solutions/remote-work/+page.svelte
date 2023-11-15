<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    let pageContent: SolutionsPageContent;
    $: pageContent = {
        heroContent: {
            title: $_("solutions.remote-work.hero.title"),
            text: $_("solutions.remote-work.hero.text"),
            image: {
                src: "/assets/solutions/hero-remote.png",
                alt: $_(
                    "solutions.index.solutions.remote-work.illustration.alt"
                ),
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/remote-update.png",
                    alt: $_(
                        "solutions.remote-work.features.feature-1.illustration.alt"
                    ),
                },
                title: $_("solutions.remote-work.features.feature-1.title"),
                text: $_("solutions.remote-work.features.feature-1.text"),
            },
            {
                image: {
                    position: "left",
                    src: "/assets/landing/notifications.png",
                    alt: $_(
                        "solutions.remote-work.features.feature-2.illustration.alt"
                    ),
                },
                title: $_("solutions.remote-work.features.feature-2.title"),
                text: $_("solutions.remote-work.features.feature-2.text"),
            },
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/remote-tasks.png",
                    alt: $_(
                        "solutions.remote-work.features.feature-3.illustration.alt"
                    ),
                },
                title: $_("solutions.remote-work.features.feature-3.title"),
                text: $_("solutions.remote-work.features.feature-3.text"),
            },
        ],
    };
</script>

<SolutionsPage {pageContent} />
