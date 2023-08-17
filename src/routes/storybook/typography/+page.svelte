<script lang="ts">
    import { anchorSizes } from "$lib/figma/types";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
</script>

{#each anchorSizes as size}
    <div id={size}>
        <Anchor {size} label="link" href={`#${size}`} />
    </div>
{/each}
