<script lang="ts">
    import { _, json } from "svelte-i18n";

    import Layout from "$lib/components/help/Layout.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    $: heroContent = {
        title: $_("help.basics.title"),
        text: $_("help.basics.description"),
    } satisfies SolutionsHeroContent;

    $: sections = $json("help.basics.sections") as {
        id: string;
        content: string;
        title: string;
    }[];
</script>

<Layout {heroContent} {sections} />
