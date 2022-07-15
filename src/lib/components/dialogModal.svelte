<script context="module" lang="ts">
    let onTop: HTMLElement;
    type Modal = {
        open: (_data?: any) => Promise<any> | null;
        close: (retVal?: any) => any;
        getData: () => any;
    };
    const modals = new Map<string, Modal>();

    export function getModal(id = ""): Modal {
        const modal = modals.get(id);
        if (!modal) {
            throw new Error("Expected modal");
        }
        return modal;
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

    let data: any | null = null;
    function getData(): any | null {
        return data;
    }

    function open(_data?: any) {
        if (visible) {
            return null;
        }
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

    const modal = { open, close, getData };
    modals.set(id, modal);
    setContext("modal", modal);

    onDestroy(() => {
        modals.delete(id);
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
