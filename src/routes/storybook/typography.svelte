<script lang="ts">
    import Anchor from "$lib/figma/Anchor.svelte";
    import { anchorSizes } from "$lib/figma/types";
</script>

{#each anchorSizes as size}
    <Anchor {size} label="link" href={`#${size}`} />
{/each}
