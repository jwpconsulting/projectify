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

    import HeroPersonal from "../assets/hero-personal.png";
    import PersonalSubTask from "../assets/personal-sub-task.png";
    import PersonalTaskCollab from "../assets/personal-task-collab.png";
    import PersonalTasks from "../assets/personal-tasks.png";

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
