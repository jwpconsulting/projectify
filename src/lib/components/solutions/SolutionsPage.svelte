<script lang="ts">
    import SolutionsFeature from "$lib/components/solutions/SolutionsFeature.svelte";
    import SolutionsHero from "$lib/components/solutions/SolutionsHero.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    import Layout from "./Layout.svelte";

    export let pageContent: SolutionsPageContent;
</script>

<Layout>
    <SolutionsHero slot="hero" heroContent={pageContent.heroContent} />

    <svelte:fragment slot="content">
        {#each pageContent.features as feature}
            <SolutionsFeature {feature} />
        {/each}
    </svelte:fragment>
</Layout>
