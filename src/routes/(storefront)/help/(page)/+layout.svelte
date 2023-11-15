<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/components/solutions/Layout.svelte";
    import SolutionsHero from "$lib/components/solutions/SolutionsHero.svelte";
    import HelpDropdown from "$lib/figma/dropdown/HelpDropdown.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

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
    <!-- TODO just a placeholder -->
    <!-- Might have to put all this inside the help layout instead -->
    <SolutionsHero slot="hero" {heroContent} />
    <div slot="side" class="grow sm:max-w-xs">
        <HelpDropdown />
    </div>
    <div slot="content" class="flex flex-col gap-4">
        <slot />
    </div>
</Layout>
