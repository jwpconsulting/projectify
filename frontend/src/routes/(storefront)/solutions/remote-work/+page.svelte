<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
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
