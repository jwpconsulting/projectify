<script lang="ts">
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";

    interface Crumb {
        href?: string;
        label: string;
    }
    export let crumbs: Crumb[];
</script>

<div class="text-sm font-bold text-utility">
    {#each crumbs as crumb, ix}
        <!-- TODO a11y make this AT compatible -->
        {#if ix > 0}
            {" "}
            &gt;
        {/if}
        {#if crumb.href}
            <Anchor label={crumb.label} size="small" href={crumb.href} />
        {:else}
            <span>{crumb.label}</span>
        {/if}
    {/each}
</div>
