<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import SolutionsHero from "$lib/components/solutions/SolutionsHero.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    export let heroContent: SolutionsHeroContent;
    export let sections: { id: string; content: string; title: string }[];

    interface HelpItem {
        title: string;
        href: string;
    }
    let helpItems: HelpItem[];
    $: helpItems = [
        {
            title: $_("help.overview"),
            href: "/help",
        },
        {
            title: $_("help.basics.title"),
            href: "/help/basics",
        },
        {
            title: $_("help.workspaces.title"),
            href: "/help/workspaces",
        },
        {
            title: $_("help.workspace-boards.title"),
            href: "/help/workspace-boards",
        },
        {
            title: $_("help.workspace-board-sections.title"),
            href: "/help/workspace-board-sections",
        },
        {
            title: $_("help.tasks.title"),
            href: "/help/tasks",
        },
        {
            title: $_("help.labels.title"),
            href: "/help/labels",
        },
        {
            title: $_("help.workspace-users.title"),
            href: "/help/workspace-users",
        },
        {
            title: $_("help.filters.title"),
            href: "/help/filters",
        },
        {
            title: $_("help.billing.title"),
            href: "/help/billing",
        },
    ];
</script>

<HeroLayout>
    <SolutionsHero slot="hero" {heroContent} />
    <nav slot="side" class="flex grow flex-col gap-4 sm:max-w-xs">
        <h2 class="text-3xl font-bold">
            {$_("help.help-sections")}
        </h2>
        <!-- sections -->
        <ul class="flex min-w-max list-inside list-disc flex-col gap-2">
            {#each helpItems as helpItem}
                <li>
                    <Anchor href={helpItem.href} label={helpItem.title} />
                </li>
            {/each}
        </ul>
    </nav>
    <div slot="content" class="flex flex-col gap-4">
        <h2 class="text-4xl font-bold">{heroContent.title}</h2>
        <!-- skip links -->
        <nav class="flex flex-col gap-4">
            <h3 class="text-xl font-bold">{$_("help.skip")}</h3>
            <ul class="flex list-inside list-disc flex-col gap-1">
                {#each sections as section}
                    <li>
                        <Anchor
                            href={`#${section.id}`}
                            label={section.title}
                        />
                    </li>
                {/each}
            </ul>
        </nav>
        <main class="flex flex-col gap-2">
            {#each sections as section}
                <section id={section.id} class="flex flex-col gap-4">
                    <h3 class="text-3xl font-bold">{section.title}</h3>
                    <p>
                        {section.content}
                    </p>
                </section>
            {/each}
        </main>
    </div>
</HeroLayout>
