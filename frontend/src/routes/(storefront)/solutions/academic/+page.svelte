<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    import AcademicSubTask from "../assets/academic-sub-task.png?enhanced";
    import HeroAcademic from "../assets/hero-academic.png?enhanced";

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
                    position: "left",
                    src: AcademicSubTask,
                    alt: $_(
                        "solutions.academic.features.feature-2.illustration.alt",
                    ),
                },
                title: $_("solutions.academic.features.feature-2.title"),
                text: $_("solutions.academic.features.feature-2.text"),
            },
        ],
    } satisfies SolutionsPageContent;
</script>

<SolutionsPage {pageContent} />
