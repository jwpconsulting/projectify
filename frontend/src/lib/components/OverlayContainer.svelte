<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { onMount } from "svelte";
    import type { Readable } from "svelte/store";

    import { handleKey } from "$lib/utils/keyboard";
    import type { Overlay } from "$lib/types/ui";
    import { keepFocusInside } from "$lib/utils/focus";

    export let store: Readable<Overlay<unknown>>;
    // method used to close this overlay
    export let closeOverlay: () => void;

    const fixed = true;

    let overlayElement: HTMLElement;

    interface Unsubscribers {
        removeEscapeListener: () => void;
        removeFocusTrap: () => void;
    }
    let unsubscribers: Unsubscribers | undefined = undefined;

    function cleanup() {
        if (unsubscribers) {
            unsubscribers.removeEscapeListener();
            unsubscribers.removeFocusTrap();
            unsubscribers = undefined;
        }
    }

    onMount(() => {
        return store.subscribe(($store) => {
            if ($store.kind === "visible") {
                console.debug("overlay visible now", overlayElement);
                unsubscribers = {
                    removeFocusTrap: keepFocusInside(overlayElement),
                    removeEscapeListener: handleKey("Escape", closeOverlay),
                };
            } else {
                cleanup();
            }
        });
    });

    onMount(() => {
        return cleanup;
    });
</script>

{#if $$slots.else}
    <div
        class="flex h-full grow flex-col"
        class:hidden={$store.kind !== "hidden"}
    >
        <slot name="else" />
    </div>
{/if}
<!-- This is how we catch the focus leaving the contex menu for a focusable
    element after this. If this is inside an iframe or something, we could
    accidentally leave the iframe... -->
<button class="fixed h-0 w-0" aria-hidden="true" />
<div
    bind:this={overlayElement}
    class="left-0 flex items-center justify-center bg-black/50"
    class:hidden={$store.kind === "hidden"}
    class:fixed={$store.kind === "visible"}
    class:top-0={fixed}
    class:h-screen={fixed}
    class:w-screen={fixed}
    class:absolute={!fixed}
    class:-top-0.5={!fixed}
    class:h-full={!fixed}
    class:w-full={!fixed}
>
    {#if $store.kind === "visible"}
        <slot target={$store.target} />
    {/if}
</div>
<!-- This is how we catch the focus leaving the contex menu for a focusable
    element after this. If this is inside an iframe or something, we could
    accidentally leave the iframe... -->
<button class="fixed h-0 w-0" aria-hidden="true" />
