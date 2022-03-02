<script>
    import { gotoDashboard } from "$lib/stores/dashboard";
    import { _ } from "svelte-i18n";

    import IconArrowLeft from "./icons/icon-arrow-left.svelte";
    export let title;
    export let loading = false;
    export let onBack = () => {
        gotoDashboard();
    };
</script>

<div class="page page-center p-8">
    <div class="w-full max-w-xl space-y-8">
        <div class="flex space-x-5 justify-start items-center">
            <button
                class="btn btn-circle btn-primary shadow-md"
                on:click={() => onBack()}
            >
                <div class="translate-x-1">
                    <IconArrowLeft />
                </div>
            </button>
            <div class="font-bold text-2xl">{title}</div>
        </div>
        {#if loading}
            <div class="text-center">{$_("loading")}</div>
        {:else}
            <div class="card shadow-card min-h-8 overflow-visible p-4">
                <slot />
            </div>
        {/if}
    </div>
</div>
