<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    import DevelopmentTeamsFilter from "../assets/development-teams-filter.png?enhanced";
    import DevelopmentTeamsTasks from "../assets/development-teams-tasks.png?enhanced";
    import HeroDevelopmentTeams from "../assets/hero-development-teams.png?enhanced";

    $: pageContent = {
        heroContent: {
            title: $_("solutions.development.hero.title"),
            text: $_("solutions.development.hero.text"),
            image: {
                src: HeroDevelopmentTeams,
                alt: $_(
                    "solutions.index.solutions.development.illustration.alt",
                ),
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: DevelopmentTeamsFilter,
                    alt: $_(
                        "solutions.development.features.feature-1.illustration.alt",
                    ),
                },
                title: $_("solutions.development.features.feature-1.title"),
                text: $_("solutions.development.features.feature-1.text"),
            },
            {
                image: {
                    position: "right",
                    src: DevelopmentTeamsTasks,
                    alt: $_(
                        "solutions.development.features.feature-3.illustration.alt",
                    ),
                },
                title: $_("solutions.development.features.feature-3.title"),
                text: $_("solutions.development.features.feature-3.text"),
            },
        ],
    } as SolutionsPageContent;
</script>

<SolutionsPage {pageContent} />
