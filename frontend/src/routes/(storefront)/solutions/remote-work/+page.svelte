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

    import HeroRemoteWork from "../assets/hero-remote-work.png?enhanced";
    import RemoteWorkTasks from "../assets/remote-work-tasks.png?enhanced";

    $: pageContent = {
        heroContent: {
            title: $_("solutions.remote-work.hero.title"),
            text: $_("solutions.remote-work.hero.text"),
            image: {
                src: HeroRemoteWork,
                alt: $_(
                    "solutions.index.solutions.remote-work.illustration.alt",
                ),
            },
        },
        features: [
            {
                image: {
                    position: "right",
                    src: RemoteWorkTasks,
                    alt: $_(
                        "solutions.remote-work.features.feature-3.illustration.alt",
                    ),
                },
                title: $_("solutions.remote-work.features.feature-3.title"),
                text: $_("solutions.remote-work.features.feature-3.text"),
            },
        ],
    } satisfies SolutionsPageContent;
</script>

<SolutionsPage {pageContent} />
