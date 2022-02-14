<script lang="ts">
    import { fly } from "svelte/transition";

    export let open = false;
    let contentWidth;

    $: {
        if (open) {
            document.body.style.overflow = "hidden";
        } else {
            document.body.style.overflow = "";
        }
    }
</script>

<div
    class:open
    class="d-modal fixed top-0 left-0 w-full h-full flex flex-col items-end justify-center p-0"
>
    <div
        on:click={() => (open = !open)}
        class="d-modal-background fixed w-full h-full bg-[#002332] open:bg-opacity-30"
    />
    {#if open}
        <div
            bind:clientWidth={contentWidth}
            transition:fly={{
                duration: 300,
                x: contentWidth,
                opacity: 1,
            }}
            class="d-modal-content bg-base-100 grow open:opacity-40"
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
        @apply opacity-30;
    }

    .d-modal > .d-modal-content {
        z-index: 100;
    }
</style>
