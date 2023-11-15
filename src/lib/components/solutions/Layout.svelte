<script lang="ts"></script>

<!-- Common layout for solution layouts -->
<div class="flex flex-col items-center gap-20 bg-foreground pb-20">
    <div class="flex w-full flex-col items-center bg-background p-6 sm:p-16">
        <div class="w-full max-w-3xl">
            <slot name="hero" />
        </div>
    </div>
    {#if $$slots.side}
        <div
            class="flex w-full max-w-5xl grow flex-col gap-4 bg-foreground p-6 sm:flex-row sm:gap-8"
        >
            <slot name="side" />
            <slot name="content" />
        </div>
    {:else}
        <div class="w-full max-w-3xl p-6">
            <slot name="content" />
        </div>
    {/if}
</div>
