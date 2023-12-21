<script lang="ts">
    export let heroBackground = true;
    export let isProseContent = false;
</script>

<!-- Common layout for solution layouts -->
<main
    class="flex flex-col items-center gap-10 bg-foreground pb-20"
    class:pt-10={!$$slots.hero}
>
    {#if $$slots.hero}
        <div
            class="flex w-full flex-col items-center bg-background"
            class:bg-background={heroBackground}
        >
            <div class="w-full max-w-4xl px-6 py-6 sm:py-12">
                <slot name="hero" />
            </div>
        </div>
    {/if}
    {#if $$slots.side}
        <div
            class="flex w-full max-w-5xl grow flex-col gap-4 bg-foreground p-6 sm:flex-row sm:gap-8"
        >
            <slot name="side" />
            <slot name="content" />
        </div>
    {:else}
        <div
            class="w-full p-6"
            class:w-full={!isProseContent}
            class:max-w-4xl={!isProseContent}
        >
            <slot name="content" />
        </div>
    {/if}
</main>
