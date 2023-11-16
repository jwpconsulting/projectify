<script lang="ts">
    import { _, json } from "svelte-i18n";

    import Layout from "$lib/components/help/Layout.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    $: heroContent = {
        title: $_("help.workspaces.title"),
        text: $_("help.workspaces.description"),
    } satisfies SolutionsHeroContent;

    $: sections = $json("help.workspaces.sections") as {
        id: string;
        content: string;
        title: string;
    }[];
</script>

<Layout {sections} {heroContent} />
