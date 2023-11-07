<script lang="ts">
    import HelpSections from "./HelpSections.svelte";
    import SkipLinks from "./SkipLinks.svelte";

    export let sections: { id: string; content: string; title: string }[];
    export let title: string;
</script>

<h1 class="text-4xl font-bold">{title}</h1>
<SkipLinks {sections} />
<HelpSections {sections} />
