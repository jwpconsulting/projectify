<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    let pageContent: SolutionsPageContent;
    $: pageContent = {
        heroContent: {
            title: $_("solutions.project-management.hero.title"),
            text: $_("solutions.project-management.hero.text"),
            image: {
                src: "/assets/solutions/hero-project-management.png",
                alt: $_(
                    "solutions.index.solutions.project-management.illustration.alt"
                ),
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: "/assets/solutions/project-member.png",
                    alt: $_(
                        "solutions.project-management.features.feature-1.illustration.alt"
                    ),
                },
                title: $_(
                    "solutions.project-management.features.feature-1.title"
                ),
                text: $_(
                    "solutions.project-management.features.feature-1.text"
                ),
            },
            {
                image: {
                    position: "left",
                    src: "/assets/landing/notifications.png",
                    alt: $_(
                        "solutions.project-management.features.feature-2.illustration.alt"
                    ),
                },
                title: $_(
                    "solutions.project-management.features.feature-2.title"
                ),
                text: $_(
                    "solutions.project-management.features.feature-2.text"
                ),
            },
            {
                image: {
                    position: "right",
                    src: "/assets/landing/filters.png",
                    alt: $_(
                        "solutions.project-management.features.feature-3.illustration.alt"
                    ),
                },
                title: $_(
                    "solutions.project-management.features.feature-3.title"
                ),
                text: $_(
                    "solutions.project-management.features.feature-3.text"
                ),
            },
            {
                image: {
                    position: "left",
                    src: "/assets/solutions/project-permissions.png",
                    alt: $_(
                        "solutions.project-management.features.feature-4.illustration.alt"
                    ),
                },
                title: $_(
                    "solutions.project-management.features.feature-4.title"
                ),
                text: $_(
                    "solutions.project-management.features.feature-4.text"
                ),
            },
        ],
    };
</script>

<SolutionsPage {pageContent} />
