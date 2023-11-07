<script lang="ts">
    import { _, json } from "svelte-i18n";

    import Layout from "$lib/components/help/Layout.svelte";

    $: sections = $json("help.billing.sections") as {
        id: string;
        content: string;
        title: string;
    }[];
</script>

<Layout {sections} title={$_("help.billing.title")} />
