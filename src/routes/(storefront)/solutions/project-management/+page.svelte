<script lang="ts">
    import { _ } from "svelte-i18n";

    import SolutionsPage from "$lib/components/solutions/SolutionsPage.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    import Filters from "../../assets/filters.png";
    import Notifications from "../../assets/notifications.png";
    import HeroProjectManagement from "../assets/hero-project-management.png";
    import ProjectManagementPermissions from "../assets/project-management-permissions.png";
    import ProjectManagementWorkspaceUser from "../assets/project-management-workspace-user.png";

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
                    src: ProjectManagementWorkspaceUser,
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
                    position: "left",
                    src: Notifications,
                    alt: $_(
                        "solutions.project-management.features.feature-2.illustration.alt",
                    ),
                },
                title: $_(
                    "solutions.project-management.features.feature-2.title",
                ),
                text: $_(
                    "solutions.project-management.features.feature-2.text",
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
