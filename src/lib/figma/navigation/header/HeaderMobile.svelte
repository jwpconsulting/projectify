<script lang="ts">
    export let logoVisible: boolean;
</script>

<div
    class="flex flex-row items-center justify-between border-b-2 border-border bg-foreground py-4 px-2 lg:hidden"
>
    {#if logoVisible}
        <a href="/">
            <img src="/assets/logo/polylogo.svg" alt="" />
        </a>
    {/if}
    <slot />
</div>
