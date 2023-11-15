<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    let pageContent: SolutionsPageContent;
    $: pageContent = {
        heroContent: {
            title: $_("solutions.personal-use.hero.title"),
            text: $_("solutions.personal-use.hero.text"),
            image: {
                src: "/assets/solutions/hero-personal.png",
                alt: $_(
                    "solutions.index.solutions.personal-use.illustration.alt"
                ),
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/personal-tasks.png",
                    alt: $_(
                        "solutions.personal-use.features.feature-1.illustration.alt"
                    ),
                },
                title: $_("solutions.personal-use.features.feature-1.title"),
                text: $_("solutions.personal-use.features.feature-1.text"),
            },
            {
                image: {
                    position: "left",
                    src: "/assets/solutions/personal-subtask.png",
                    alt: $_(
                        "solutions.personal-use.features.feature-2.illustration.alt"
                    ),
                },
                title: $_("solutions.personal-use.features.feature-2.title"),
                text: $_("solutions.personal-use.features.feature-2.text"),
            },
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/personal-task-collab.png",
                    alt: $_(
                        "solutions.personal-use.features.feature-3.illustration.alt"
                    ),
                },
                title: $_("solutions.personal-use.features.feature-3.title"),
                text: $_("solutions.personal-use.features.feature-3.text"),
            },
        ],
    };
</script>

<SolutionsPage {pageContent} />
