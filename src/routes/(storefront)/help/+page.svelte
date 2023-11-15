<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/components/solutions/Layout.svelte";
    import SolutionsHero from "$lib/components/solutions/SolutionsHero.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    interface HelpTopic {
        title: string;
        description: string;
        href: string;
    }

    $: helpTopics = [
        {
            title: $_("help.basics.title"),
            description: $_("help.basics.description"),
            href: "/help/basics",
        },
        {
            title: $_("help.workspaces.title"),
            description: $_("help.workspaces.description"),
            href: "/help/workspaces",
        },
        {
            title: $_("help.workspace-boards.title"),
            description: $_("help.workspace-boards.description"),
            href: "/help/workspace-boards",
        },
        {
            title: $_("help.workspace-board-sections.title"),
            description: $_("help.workspace-board-sections.description"),
            href: "/help/workspace-board-sections",
        },
        {
            title: $_("help.tasks.title"),
            description: $_("help.tasks.description"),
            href: "/help/tasks",
        },
        {
            title: $_("help.labels.title"),
            description: $_("help.labels.description"),
            href: "/help/labels",
        },
        {
            title: $_("help.workspace-users.title"),
            description: $_("help.workspace-users.description"),
            href: "/help/workspace-users",
        },
        {
            title: $_("help.filters.title"),
            description: $_("help.filters.description"),
            href: "/help/filters",
        },
        {
            title: $_("help.billing.title"),
            description: $_("help.billing.description"),
            href: "/help/billing",
        },
    ] satisfies HelpTopic[];
    $: heroContent = {
        title: $_("help.hero.header.text"),
        text: $_("help.hero.header.subtext"),
        image: {
            src: "/assets/help/help-hero.png",
            alt: $_("help.hero.image.alt"),
        },
    } satisfies SolutionsHeroContent;
</script>

<Layout>
    <SolutionsHero slot="hero" {heroContent} />
    <div slot="content" class="flex flex-col gap-4">
        <div class="flex flex-col gap-6 sm:grid sm:grid-cols-2 md:grid-cols-3">
            {#each helpTopics as helpTopic}
                <section class="flex flex-col gap-2">
                    <h1 class="text-lg font-bold">
                        {helpTopic.title}
                    </h1>
                    <p>{helpTopic.description}</p>
                    <Anchor
                        href={helpTopic.href}
                        label={$_("help.go-to-section")}
                    />
                </section>
            {/each}
        </div>
    </div>
</Layout>
