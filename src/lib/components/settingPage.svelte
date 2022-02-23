<script>
    import { gotoDashboard } from "$lib/stores/dashboard";

    import IconArrowLeft from "./icons/icon-arrow-left.svelte";
    export let title;
    export let onBack = () => {
        gotoDashboard();
    };
</script>

<div class="page page-center">
    <div class="w-full max-w-xl space-y-8">
        <div class="flex space-x-5 justify-start items-center">
            <button
                class="btn btn-circle btn-primary"
                on:click={() => onBack()}
            >
                <div class="translate-x-1">
                    <IconArrowLeft />
                </div>
            </button>
            <div class="font-bold text-2xl">{title}</div>
        </div>
        <div class="card min-h-8 overflow-visible">
            <slot />
        </div>
    </div>
</div>
