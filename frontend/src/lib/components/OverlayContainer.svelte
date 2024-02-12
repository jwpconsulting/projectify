<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<script lang="ts">
    import { onMount } from "svelte";
    import type { Readable } from "svelte/store";

    import { handleKey } from "$lib/stores/globalUi";
    import type { Overlay } from "$lib/types/ui";
    import { keepFocusInside } from "$lib/utils/focus";

    import { browser } from "$app/environment";

    export let store: Readable<Overlay<unknown>>;
    // method used to close this overlay
    export let closeOverlay: () => void;

    const fixed = true;

    let overlayElement: HTMLElement;

    onMount(() => {
        if (!browser) {
            return undefined;
        }
        let unfocus: undefined | (() => void) = undefined;
        let escapeUnsubscriber: (() => void) | undefined = undefined;
        const unsubscriber = store.subscribe(($store) => {
            if ($store.kind === "visible") {
                console.log("visible now", overlayElement);
                unfocus = keepFocusInside(overlayElement);
                escapeUnsubscriber = handleKey("Escape", closeOverlay);
            } else {
                if (unfocus) {
                    unfocus();
                    unfocus = undefined;
                }
                if (escapeUnsubscriber) {
                    escapeUnsubscriber();
                    escapeUnsubscriber = undefined;
                }
            }
        });
        return () => {
            if (unfocus) {
                unfocus();
                unfocus = undefined;
            }
            if (escapeUnsubscriber) {
                escapeUnsubscriber();
                escapeUnsubscriber = undefined;
            }
            unsubscriber();
        };
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
