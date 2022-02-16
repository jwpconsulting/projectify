<script lang="ts">
    import { getContext } from "svelte";
    import { _ } from "svelte-i18n";

    export let title;
    export let cancelLabel = $_("Cancel");
    export let confirmLabel = $_("Confirm");

    const modal = getContext<any>("modal");
    function cancel() {
        modal.close();
    }
    function confirm() {
        modal.close({ confirm: true });
    }
</script>

<div class="card-body max-w-lg">
    <div class="flex flex-col divide-y divide-base-300">
        <h1 class="text-3xl font-bold text-center pb-4">{title}</h1>
        <div class="pt-4">
            <slot />
        </div>
    </div>
    <div class="flex pt-7 space-x-2 w-full">
        <button
            class="btn btn-primary btn-outline rounded-full grow"
            on:click={cancel}>{cancelLabel}</button
        >
        <button class="btn btn-accent rounded-full grow" on:click={confirm}
            >{confirmLabel}</button
        >
    </div>
</div>
