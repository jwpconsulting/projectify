<script lang="ts">
    import { browser } from "$app/env";
    import { fly } from "svelte/transition";

    export let open = false;
    let contentWidth;

    $: {
        if (browser) {
            if (open) {
                document.body.style.overflow = "hidden";
            } else {
                document.body.style.overflow = "";
            }
        }
    }
</script>

<div
    class:open
    class="d-modal fixed top-0 left-0 z-50 flex h-full w-full flex-col items-end justify-center p-0"
>
    <div
        on:click={() => (open = !open)}
        class="d-modal-background fixed h-full w-full bg-[#000]"
    />
    {#if open}
        <div
            bind:clientWidth={contentWidth}
            transition:fly={{
                duration: 300,
                x: contentWidth,
                opacity: 1,
            }}
            class="d-modal-content grow bg-base-100 open:opacity-40"
        >
            <slot />
        </div>
    {/if}
</div>

<style lang="scss">
    .d-modal {
        @apply pointer-events-none;
    }
    .d-modal.open {
        @apply pointer-events-auto;
    }
    .d-modal > .d-modal-background {
        @apply opacity-0;
        transition: all 300ms ease-in-out;
    }
    .d-modal.open > .d-modal-background {
        @apply opacity-60 backdrop-blur-sm;
    }

    .d-modal > .d-modal-content {
        z-index: 100;
    }
</style>
