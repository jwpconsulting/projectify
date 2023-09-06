<script lang="ts">
    import focusLock from "dom-focus-lock";
    import { onMount } from "svelte";
    import type { Readable } from "svelte/store";

    import { browser } from "$app/environment";
    import type { Overlay } from "$lib/types/ui";

    export let store: Readable<Overlay<unknown>>;

    export let fixed = true;

    let overlayElement: HTMLElement;

    onMount(() => {
        if (!browser) {
            return undefined;
        }
        const unsubscriber = store.subscribe(($store) => {
            if ($store.kind === "visible") {
                focusLock.on(overlayElement);
            } else {
                focusLock.off(overlayElement);
            }
        });
        return () => {
            focusLock.off(overlayElement);
            unsubscriber();
        };
    });
</script>

{#if $$slots.else}
    <div class="h-full" class:hidden={$store.kind !== "hidden"}>
        <slot name="else" />
    </div>
{/if}
{#if $store.kind === "visible"}
    <div
        bind:this={overlayElement}
        class="left-0 flex items-center justify-center bg-black/50"
        class:fixed
        class:top-0={fixed}
        class:h-screen={fixed}
        class:w-screen={fixed}
        class:absolute={!fixed}
        class:-top-0.5={!fixed}
        class:h-full={!fixed}
        class:w-full={!fixed}
    >
        <slot target={$store.target} />
    </div>
{/if}
