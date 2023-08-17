<script lang="ts">
    import SolutionsFeature from "$lib/components/solutions/SolutionsFeature.svelte";
    import SolutionsHero from "$lib/components/solutions/SolutionsHero.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    export let pageContent: SolutionsPageContent;
</script>

<div class="mb-20 flex flex-col gap-20">
    <SolutionsHero heroContent={pageContent.heroContent} />

    <div class="mx-6 flex flex-col gap-6 sm:mx-16 sm:gap-16">
        {#each pageContent.features as feature}
            <SolutionsFeature {feature} />
        {/each}
    </div>
</div>
