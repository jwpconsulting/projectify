<script lang="ts">
    import { Exclamation } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { fade } from "svelte/transition";
    import { _ } from "svelte-i18n";

    import { online } from "$lib/stores/wsSubscription";
</script>

<!-- Refactor using OverlayContainer -->
{#if !$online}
    <div
        class="bg-base fixed left-0 top-0 z-50 flex h-full w-full items-center justify-center bg-opacity-50 p-2 backdrop-blur-sm"
        transition:fade|global={{ duration: 100 }}
    >
        <div
            class="align-center flex flex-col divide-y divide-primary-content divide-opacity-50 rounded-md bg-error px-4 py-2 text-center text-primary-content shadow-md"
        >
            <div class="flex space-x-2 p-2 py-4">
                <Icon src={Exclamation} class="h-6 w-6" theme="outline" />
                <div>{$_("connection-status.disconnected")}</div>
            </div>
            <a class="link p-2 py-4 text-sm" href="/"
                >{$_("connection-status.back-to-landing")}</a
            >
        </div>
    </div>
{/if}
