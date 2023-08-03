<script lang="ts">
    import { goto } from "$app/navigation";
    import { getDashboardWorkspaceUrl } from "$lib/urls";
    import { currentWorkspaceUuid } from "$lib/stores/dashboard";

    import IconArrowLeft from "$lib/components/icons/icon-arrow-left.svelte";
    import Loading from "$lib/components/loading.svelte";

    export let title: string | null = null;
    export let loading = false;
    export let onBack = () => {
        if ($currentWorkspaceUuid) {
            goto(getDashboardWorkspaceUrl($currentWorkspaceUuid));
        }
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
            <div class="text-2xl font-bold">{title ? title : "Woops"}</div>
        </div>
        {#if loading}
            <div
                class="flex min-h-full items-center justify-center text-center"
            >
                <Loading />
            </div>
        {:else}
            <div class="card min-h-8 overflow-visible pt-6 shadow-card">
                <slot />
            </div>
        {/if}
    </div>
</div>
