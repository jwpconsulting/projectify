<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    import Filters from "../../assets/filters.png?enhanced";
    import HeroProjectManagement from "../assets/hero-project-management.png?enhanced";
    import ProjectManagementPermissions from "../assets/project-management-permissions.png?enhanced";
    import ProjectManagementTeamMember from "../assets/project-management-team-member.png?enhanced";

    $: pageContent = {
        heroContent: {
            title: $_("solutions.project-management.hero.title"),
            text: $_("solutions.project-management.hero.text"),
            image: {
                src: HeroProjectManagement,
                alt: $_(
                    "solutions.index.solutions.project-management.illustration.alt",
                ),
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: ProjectManagementTeamMember,
                    alt: $_(
                        "solutions.project-management.features.feature-1.illustration.alt",
                    ),
                },
                title: $_(
                    "solutions.project-management.features.feature-1.title",
                ),
                text: $_(
                    "solutions.project-management.features.feature-1.text",
                ),
            },
            {
                image: {
                    position: "right",
                    src: Filters,
                    alt: $_(
                        "solutions.project-management.features.feature-3.illustration.alt",
                    ),
                },
                title: $_(
                    "solutions.project-management.features.feature-3.title",
                ),
                text: $_(
                    "solutions.project-management.features.feature-3.text",
                ),
            },
            {
                image: {
                    position: "left",
                    src: ProjectManagementPermissions,
                    alt: $_(
                        "solutions.project-management.features.feature-4.illustration.alt",
                    ),
                },
                title: $_(
                    "solutions.project-management.features.feature-4.title",
                ),
                text: $_(
                    "solutions.project-management.features.feature-4.text",
                ),
            },
        ],
    } satisfies SolutionsPageContent;
</script>

<SolutionsPage {pageContent} />
