<script>
    import { gotoDashboard } from "$lib/stores/dashboard";
    import { _ } from "svelte-i18n";

    import IconArrowLeft from "./icons/icon-arrow-left.svelte";
    import Loading from "./loading.svelte";
    export let title;
    export let loading = false;
    export let onBack = () => {
        gotoDashboard();
    };
</script>

<div class="page items-center justify-start p-8">
    <div class="w-full max-w-xl space-y-8">
        <div class="flex items-center justify-start space-x-5">
            <button
                class="btn btn-primary btn-circle shadow-md"
                on:click={() => onBack()}
            >
                <div class="translate-x-1">
                    <IconArrowLeft />
                </div>
            </button>
            <div class="text-2xl font-bold">{title}</div>
        </div>
        {#if loading}
            <div
                class="flex min-h-full items-center justify-center text-center"
            >
                <Loading />
            </div>
        {:else}
            <div class="card shadow-card min-h-8 overflow-visible py-4">
                <slot />
            </div>
        {/if}
    </div>
</div>
