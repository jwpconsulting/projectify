<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
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
