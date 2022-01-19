<script context="module" lang="ts">
    let onTop;
    const modals = {};

    export function getModal(id = "") {
        return modals[id];
    }
</script>

<script lang="ts">
    import { onDestroy } from "svelte";

    let topDiv;
    let visible = false;
    let prevOnTop;
    let closeCallback;

    export let id = "";

    function keyPress(ev) {
        if (ev.key == "Escape" && onTop == topDiv) close();
    }

    function open(callback) {
        closeCallback = callback;

        if (visible) return;
        visible = true;

        prevOnTop = onTop;
        onTop = topDiv;
        window.addEventListener("keydown", keyPress);

        document.body.style.overflow = "hidden";
    }

    function close(retVal?) {
        if (!visible) return;
        window.removeEventListener("keydown", keyPress);
        onTop = prevOnTop;
        if (onTop == null) document.body.style.overflow = "";
        visible = false;
        if (closeCallback) closeCallback(retVal);
    }

    modals[id] = { open, close };

    onDestroy(() => {
        delete modals[id];
        window.removeEventListener("keydown", keyPress);
    });
</script>

<div
    class:visible
    class="d-modal fixed top-0 left-0 w-full h-full flex flex-col items-center justify-center p-0"
    bind:this={topDiv}
>
    <div
        on:click={() => close(null)}
        class="d-modal-background fixed w-full h-full bg-[#002332] open:bg-opacity-30"
    />
    <div class="d-modal-content bg-base-100 open:opacity-40">
        <slot />
    </div>
</div>

<style lang="scss">
    .d-modal {
        @apply pointer-events-none;
    }
    .d-modal.visible {
        @apply pointer-events-auto;
    }
    .d-modal > .d-modal-background {
        @apply opacity-0;
        transition: all 300ms ease-in-out;
    }
    .d-modal.visible > .d-modal-background {
        @apply opacity-30;
    }

    .d-modal > .d-modal-content {
        transform: translateY(-30px);
        opacity: 0;
        transition: all 300ms ease-in-out;
    }
    .d-modal.visible > .d-modal-content {
        opacity: 1;
        transform: translateY(0);
    }
</style>
