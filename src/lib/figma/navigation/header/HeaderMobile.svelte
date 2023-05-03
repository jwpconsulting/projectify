<script lang="ts">
    export let logoVisible: boolean;
</script>

<div
    class="flex flex-row items-center justify-between border-b-2 border-border bg-foreground px-2 py-4 lg:hidden"
>
    {#if logoVisible}
        <a href="/">
            <img src="/assets/logo/polylogo.svg" alt="" />
        </a>
    {/if}
    <slot />
</div>
