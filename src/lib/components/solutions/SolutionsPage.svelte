<script lang="ts">
    import Hero from "$lib/components/layouts/Hero.svelte";
    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import SolutionsFeature from "$lib/components/solutions/SolutionsFeature.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    export let pageContent: SolutionsPageContent;
</script>

<HeroLayout>
    <Hero slot="hero" heroContent={pageContent.heroContent} />

    <div
        slot="content"
        class="flex w-full flex-col items-center gap-6 sm:gap-16"
    >
        {#each pageContent.features as feature}
            <SolutionsFeature {feature} />
        {/each}
    </div>
</HeroLayout>
