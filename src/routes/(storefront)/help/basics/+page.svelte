<script lang="ts">
    import { json } from "svelte-i18n";

    import HelpSections from "$lib/components/help/HelpSections.svelte";
    import SkipLinks from "$lib/components/help/SkipLinks.svelte";

    $: sections = $json("help.basics.sections") as {
        id: string;
        content: string;
        title: string;
    }[];
</script>

<SkipLinks {sections} />
<HelpSections {sections} />
