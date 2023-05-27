<script lang="ts">
    import Continue from "$lib/figma/navigation/header/Continue.svelte";
    import Landing from "$lib/figma/navigation/header/Landing.svelte";
    import { user } from "$lib/stores/user";
</script>

<div class="flex flex-col">
    {#if user}
        <Continue />
    {:else}
        <Landing />
    {/if}
    <slot />
</div>
