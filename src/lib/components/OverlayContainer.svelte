<script lang="ts">
    import { onMount } from "svelte";
    import type { Readable } from "svelte/store";

    import { browser } from "$app/environment";
    import type { Overlay } from "$lib/types/ui";
    import { keepFocusInside } from "$lib/utils/focus";

    export let store: Readable<Overlay<unknown>>;

    export let fixed = true;

    let overlayElement: HTMLElement;

    onMount(() => {
        if (!browser) {
            return undefined;
        }
        let unfocus: undefined | (() => void) = undefined;
        const unsubscriber = store.subscribe(($store) => {
            if ($store.kind === "visible") {
                console.log("visible now", overlayElement);
                unfocus = keepFocusInside(overlayElement);
            } else {
                if (unfocus) {
                    unfocus();
                    unfocus = undefined;
                }
            }
        });
        return () => {
            if (unfocus) {
                unfocus();
                unfocus = undefined;
            }
            unsubscriber();
        };
    });
</script>

{#if $$slots.else}
    <div class="h-full" class:hidden={$store.kind !== "hidden"}>
        <slot name="else" />
    </div>
{/if}
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
