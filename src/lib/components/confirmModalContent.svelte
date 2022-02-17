<script lang="ts">
    import { getContext } from "svelte";
    import { _ } from "svelte-i18n";

    export let title;
    export let cancelLabel = $_("Cancel");
    export let confirmLabel = $_("Confirm");
    export let confirmColor = "primary";

    export let inputs = [];

    const modal = getContext<any>("modal");
    function cancel() {
        modal.close();
    }
    function confirm() {
        const outputs = {};
        inputs.forEach((out) => {
            outputs[out.name] = out.value;
        });

        modal.close({ confirm: true, outputs });
    }
</script>

<div class="card-body max-w-lg">
    <div
        class="flex flex-col {inputs.length
            ? ''
            : 'divide-y divide-base-300'}}"
    >
        <h1 class="text-3xl font-bold text-center pb-4">{title}</h1>
        <div class="pt-4">
            <slot />
        </div>
    </div>
    {#each inputs as input}
        <div class="form-control w-full">
            <label for={input.name} class="label label-text uppercase"
                >{input.label}</label
            >
            <input
                type="text"
                name={input.name}
                placeholder={`${$_("please-enter-a")} ${input.label}`}
                class="input input-bordered"
                bind:value={input.value}
            />
        </div>
    {/each}
    <div class="flex pt-9 space-x-2 w-full">
        <button
            class="btn btn-primary btn-outline rounded-full grow"
            on:click|preventDefault={cancel}>{cancelLabel}</button
        >
        <button
            class="btn btn-{confirmColor} rounded-full grow"
            on:click|preventDefault={confirm}>{confirmLabel}</button
        >
    </div>
</div>
