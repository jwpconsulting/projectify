<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    import AcademicPopup from "../assets/academic-popup.png";
    import AcademicSubTask from "../assets/academic-sub-task.png";
    import AcademicUpdate from "../assets/academic-update.png";
    import HeroAcademic from "../assets/hero-academic.png";

    $: pageContent = {
        heroContent: {
            title: $_("solutions.academic.hero.title"),
            text: $_("solutions.academic.hero.text"),
            image: {
                src: HeroAcademic,
                alt: $_("solutions.index.solutions.academic.illustration.alt"),
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: AcademicPopup,
                    alt: $_(
                        "solutions.academic.features.feature-1.illustration.alt",
                    ),
                },
                title: $_("solutions.academic.features.feature-1.title"),
                text: $_("solutions.academic.features.feature-1.text"),
            },
            {
                image: {
                    position: "left",
                    src: AcademicSubTask,
                    alt: $_(
                        "solutions.academic.features.feature-2.illustration.alt",
                    ),
                },
                title: $_("solutions.academic.features.feature-2.title"),
                text: $_("solutions.academic.features.feature-2.text"),
            },
            {
                image: {
                    position: "right",
                    src: AcademicUpdate,
                    alt: $_(
                        "solutions.academic.features.feature-3.illustration.alt",
                    ),
                },
                title: $_("solutions.academic.features.feature-3.title"),
                text: $_("solutions.academic.features.feature-3.text"),
            },
        ],
    } satisfies SolutionsPageContent;
</script>

<SolutionsPage {pageContent} />
