<script lang="ts">
    import { fade } from "svelte/transition";
    import { _ } from "svelte-i18n";
    import {
        activeWSConnections,
        activeWSSubscriptions,
        online,
    } from "$lib/stores/wsSubscription";
    import IconsExclamation from "$lib/components/icons/icons-exclamation.svelte";
</script>

{#if $activeWSSubscriptions != $activeWSConnections || ($online == false && $activeWSSubscriptions > 0)}
    <div
        class="bg-base fixed left-0 top-0 z-50 flex h-full w-full items-center justify-center bg-opacity-50 p-2 backdrop-blur-sm"
        transition:fade={{ duration: 100 }}
    >
        <div
            class="align-center flex flex-col divide-y divide-primary-content divide-opacity-50 rounded-md bg-error px-4 py-2 text-center text-primary-content shadow-md"
        >
            <div class="flex space-x-2 p-2 py-4">
                <div><IconsExclamation /></div>
                <div>{$_("disconnected-network")}</div>
            </div>
            <a class="link p-2 py-4 text-sm" href="/"
                >{$_("back-to-landing-page")}</a
            >
        </div>
    </div>
{/if}
