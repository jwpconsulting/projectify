<script lang="ts">
    import SolutionsFeature from "$lib/components/solutions/SolutionsFeature.svelte";
    import SolutionsHero from "$lib/components/solutions/SolutionsHero.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    export let pageContent: SolutionsPageContent;
</script>

<div class="flex flex-col items-center gap-20 pb-20">
    <SolutionsHero heroContent={pageContent.heroContent} />

    <div class="flex max-w-3xl flex-col gap-6 px-8 sm:mx-16 sm:gap-16">
        {#each pageContent.features as feature}
            <SolutionsFeature {feature} />
        {/each}
    </div>
</div>
