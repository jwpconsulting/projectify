<script lang="ts">
    import { _, json } from "svelte-i18n";

    import Layout from "$lib/components/help/Layout.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    $: heroContent = {
        title: $_("help.billing.title"),
        text: $_("help.billing.description"),
    } satisfies SolutionsHeroContent;

    $: sections = $json("help.billing.sections") as {
        id: string;
        content: string;
        title: string;
    }[];
</script>

<Layout {heroContent} {sections} />
