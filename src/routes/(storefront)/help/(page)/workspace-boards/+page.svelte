<script lang="ts">
    import { _, json } from "svelte-i18n";

    import Layout from "$lib/components/help/Layout.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    $: heroContent = {
        title: $_("help.workspace-boards.title"),
        text: $_("help.workspace-boards.description"),
    } satisfies SolutionsHeroContent;

    $: sections = $json("help.workspace-boards.sections") as {
        id: string;
        content: string;
        title: string;
    }[];
</script>

<Layout {heroContent} {sections} />
