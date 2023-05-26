<script lang="ts">
    export let logoVisibleDesktop = false;
    export let logoVisibleMobile = false;
</script>

<div
    class="hidden flex-row items-center justify-between border-b-2 border-border bg-foreground px-6 py-4 lg:flex"
>
    <div class="flex flex-row items-center gap-12">
        {#if logoVisibleDesktop}
            <a href="/">
                <img src="/assets/logo/polylogo.svg" alt="" />
            </a>
        {/if}
        <slot name="desktop-left" />
    </div>
    <slot name="center" />
    <div class="flex flex-row gap-6">
        <slot name="desktop-right" />
    </div>
</div>

<div
    class="flex flex-row items-center justify-between border-b-2 border-border bg-foreground px-2 py-4 lg:hidden"
>
    {#if logoVisibleMobile}
        <a href="/">
            <img src="/assets/logo/polylogo.svg" alt="" />
        </a>
    {/if}
    <slot name="mobile" />
</div>
