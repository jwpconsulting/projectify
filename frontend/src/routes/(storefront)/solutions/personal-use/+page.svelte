<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    import HeroPersonal from "../assets/hero-personal.png?enhanced";
    import PersonalSubTask from "../assets/personal-sub-task.png?enhanced";
    import PersonalTaskCollab from "../assets/personal-task-collab.png?enhanced";
    import PersonalTasks from "../assets/personal-tasks.png?enhanced";

    $: pageContent = {
        heroContent: {
            title: $_("solutions.personal-use.hero.title"),
            text: $_("solutions.personal-use.hero.text"),
            image: {
                src: HeroPersonal,
                alt: $_(
                    "solutions.index.solutions.personal-use.illustration.alt",
                ),
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: PersonalTasks,
                    alt: $_(
                        "solutions.personal-use.features.feature-1.illustration.alt",
                    ),
                },
                title: $_("solutions.personal-use.features.feature-1.title"),
                text: $_("solutions.personal-use.features.feature-1.text"),
            },
            {
                image: {
                    position: "left",
                    src: PersonalSubTask,
                    alt: $_(
                        "solutions.personal-use.features.feature-2.illustration.alt",
                    ),
                },
                title: $_("solutions.personal-use.features.feature-2.title"),
                text: $_("solutions.personal-use.features.feature-2.text"),
            },
            {
                image: {
                    position: "right",
                    src: PersonalTaskCollab,
                    alt: $_(
                        "solutions.personal-use.features.feature-3.illustration.alt",
                    ),
                },
                title: $_("solutions.personal-use.features.feature-3.title"),
                text: $_("solutions.personal-use.features.feature-3.text"),
            },
        ],
    } satisfies SolutionsPageContent;
</script>

<SolutionsPage {pageContent} />
