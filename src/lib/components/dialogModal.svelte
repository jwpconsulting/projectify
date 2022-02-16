<script context="module" lang="ts">
    let onTop;
    const modals = {};

    export function getModal(id = "") {
        return modals[id];
    }
</script>

<script lang="ts">
    import { onDestroy, setContext } from "svelte";

    import { fly } from "svelte/transition";

    let topDiv;
    let visible = false;
    let prevOnTop;

    export let id = "";

    function keyPress(ev) {
        if (ev.key == "Escape" && onTop == topDiv) close();
    }

    let resolveFn;

    function open() {
        if (visible) return;
        visible = true;

        prevOnTop = onTop;
        onTop = topDiv;
        window.addEventListener("keydown", keyPress);
        document.body.style.overflow = "hidden";

        return new Promise((res) => {
            resolveFn = res;
        });
    }

    function close(retVal?) {
        if (!visible) return;
        window.removeEventListener("keydown", keyPress);
        onTop = prevOnTop;

        if (onTop == null) document.body.style.overflow = "";

        visible = false;
        if (resolveFn) {
            resolveFn(retVal);
        }
    }

    modals[id] = { open, close };
    setContext("modal", modals[id]);

    onDestroy(() => {
        delete modals[id];
        window.removeEventListener("keydown", keyPress);
    });
</script>

{#if visible}
    <div
        class="d-modal fixed top-0 left-0 w-full h-full flex flex-col items-center justify-center p-0"
        bind:this={topDiv}
    >
        <div
            transition:fly={{ duration: 500, opacity: 0 }}
            on:click={() => close(null)}
            class="d-modal-background fixed w-full h-full bg-[#002332] bg-opacity-30"
        />
        <div
            in:fly={{ duration: 300, y: -50, opacity: 0 }}
            out:fly={{ duration: 300, y: 50, opacity: 0 }}
            class="d-modal-content bg-base-100 open:opacity-40 card shadow-card"
        >
            <slot />
        </div>
    </div>
{/if}
