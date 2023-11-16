<script lang="ts">
    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import SolutionsHero from "$lib/components/solutions/SolutionsHero.svelte";
    import HelpDropdown from "$lib/figma/dropdown/HelpDropdown.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    import HelpSections from "./HelpSections.svelte";
    import SkipLinks from "./SkipLinks.svelte";

    export let heroContent: SolutionsHeroContent;
    export let sections: { id: string; content: string; title: string }[];
</script>

<HeroLayout>
    <!-- TODO just a placeholder -->
    <!-- Might have to put all this inside the help layout instead -->
    <SolutionsHero slot="hero" {heroContent} />
    <div slot="side" class="grow sm:max-w-xs">
        <HelpDropdown />
    </div>
    <div slot="content" class="flex flex-col gap-4">
        <h2 class="text-4xl font-bold">{heroContent.title}</h2>
        <SkipLinks {sections} />
        <HelpSections {sections} />
    </div>
</HeroLayout>
