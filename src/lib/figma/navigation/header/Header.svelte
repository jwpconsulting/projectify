<script lang="ts">
    export let logoVisible: boolean;
</script>

<div
    class="hidden flex-row items-center justify-between border-b-2 border-border bg-foreground py-4 px-6 lg:flex"
>
    <div class="flex flex-row items-center gap-12">
        {#if logoVisible}
            <a href="/">
                <img src="/assets/logo/polylogo.svg" alt="" />
            </a>
        {/if}
        <slot name="left" />
    </div>
    <div class="flex flex-row gap-6">
        <slot name="right" />
    </div>
</div>
