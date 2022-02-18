<script lang="ts">
    import { getContext } from "svelte";
    import { _ } from "svelte-i18n";

    export let title;
    export let cancelLabel = $_("Cancel");
    export let confirmLabel = $_("Confirm");
    export let confirmColor = "primary";

    export let inputs = [];
    let isEditing = false;

    const modal = getContext<any>("modal");
    $: data = modal.getData();

    $: {
        if (!isEditing) {
            inputs.forEach((input) => {
                input.value = data[input.name];
            });
        }
    }

    function cancel() {
        modal.close();
        isEditing = false;
    }
    function confirm() {
        const outputs = {};
        inputs.forEach((out) => {
            outputs[out.name] = out.value;
        });

        modal.close({ confirm: true, outputs });
        isEditing = false;
    }
</script>

<div class="card-body w-screen max-w-lg">
    <div class:divide-y={!inputs.length} class="flex flex-col divide-base-300">
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
                on:input={() => (isEditing = true)}
            />
        </div>
    {/each}
    <div class="flex pt-9 space-x-2 w-full">
        <button
            class="btn btn-primary btn-outline rounded-full grow"
            on:click|preventDefault={cancel}>{cancelLabel}</button
        >
        <button
            class:btn-primary={confirmColor == "primary"}
            class:btn-accent={confirmColor == "accent"}
            class="btn rounded-full grow"
            on:click|preventDefault={confirm}>{confirmLabel}</button
        >
    </div>
</div>
