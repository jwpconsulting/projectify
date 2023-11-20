<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import SolutionsHero from "$lib/components/solutions/SolutionsHero.svelte";
    import HelpDropdown from "$lib/figma/dropdown/HelpDropdown.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    import HelpSections from "./HelpSections.svelte";

    export let heroContent: SolutionsHeroContent;
    export let sections: { id: string; content: string; title: string }[];
</script>

<HeroLayout>
    <SolutionsHero slot="hero" {heroContent} />
    <div slot="side" class="grow sm:max-w-xs">
        <HelpDropdown />
    </div>
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
        <HelpSections {sections} />
    </div>
</HeroLayout>
