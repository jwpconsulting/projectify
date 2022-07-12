<script context="module" lang="ts">
    let onTop: HTMLElement;
    const modals = {};

    export function getModal(id = "") {
        return modals[id];
    }
</script>

<script lang="ts">
    import { onDestroy, setContext } from "svelte";

    import { fly } from "svelte/transition";

    let topDiv: HTMLElement;
    let visible = false;
    let prevOnTop: HTMLElement;

    export let id = "";

    function keyPress(ev: KeyboardEvent) {
        if (ev.key == "Escape" && onTop == topDiv) close();
    }

    let resolveFn: (_: any) => void;

    let data = null;
    function getData() {
        return data;
    }

    function open(_data?: any) {
        if (visible) return;
        visible = true;

        data = _data;

        prevOnTop = onTop;
        onTop = topDiv;
        window.addEventListener("keydown", keyPress);
        document.body.style.overflow = "hidden";

        return new Promise((res) => {
            resolveFn = res;
        });
    }

    function close(retVal?: any) {
        if (!visible) return;
        window.removeEventListener("keydown", keyPress);
        onTop = prevOnTop;

        if (onTop == null) document.body.style.overflow = "";

        visible = false;
        if (resolveFn) {
            resolveFn(retVal);
        }
    }

    modals[id] = { open, close, getData };
    setContext("modal", modals[id]);

    onDestroy(() => {
        delete modals[id];
        window.removeEventListener("keydown", keyPress);
    });
</script>

{#if visible}
    <div
        class="d-modal fixed top-0 left-0 z-50 flex h-full w-full flex-col items-center justify-center p-0"
        bind:this={topDiv}
    >
        <div
            transition:fly={{ duration: 500, opacity: 0 }}
            on:click={() => close(null)}
            class="d-modal-background fixed h-full w-full bg-[#000] bg-opacity-60"
        />
        <div
            in:fly={{ duration: 300, y: -50, opacity: 0 }}
            out:fly={{ duration: 300, y: 50, opacity: 0 }}
            class="d-modal-content card bg-base-100 shadow-card open:opacity-40"
        >
            <slot />
        </div>
    </div>
{/if}
