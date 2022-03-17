<script lang="ts">
    import { getContext } from "svelte";
    import { _ } from "svelte-i18n";
    import ColorPicker from "./colorPicker.svelte";

    export let title;
    export let subtitle = null;
    export let cancelLabel = $_("Cancel");
    export let confirmLabel = $_("Confirm");
    export let confirmColor = "primary";

    export let inputs = [];
    let isEditing = false;

    const modal = getContext<any>("modal");
    $: data = modal.getData();

    $: {
        if (data && !isEditing) {
            inputs.forEach((input) => {
                input.value = data[input.name];
            });
        }
    }

    function cancel() {
        modal.close();
        isEditing = false;
    }

    let valid = true;

    function confirm() {
        const outputs = {};

        inputs.forEach((field) => {
            if (
                field.validation?.required &&
                (field.value === "" ||
                    field.value === null ||
                    field.value === undefined)
            ) {
                valid = false;
                field.error = $_("this-field-is-required");
            }

            outputs[field.name] = field.value;
        });

        if (!valid) {
            return;
        }

        modal.close({ confirm: true, outputs });
        isEditing = false;
    }

    function placeholderFor(input) {
        if (input.placeholder) {
            return input.placeholder;
        }
        return `${$_("please-enter-a")} ${input.label}`;
    }
</script>

<div class="card-body w-screen max-w-lg">
    <div class:divide-y={!inputs.length} class="flex flex-col divide-base-300">
        <h1 class="text-3xl font-bold text-center pb-4">{title}</h1>
        {#if subtitle}
            <div class="text-center">{subtitle}</div>
        {/if}
        <div class="pt-4">
            <slot />
        </div>
    </div>
    {#each inputs as input}
        <div class="form-control w-full">
            <label for={input.name} class="label label-text uppercase"
                >{input.label}</label
            >
            {#if input.type == "colorPicker"}
                <ColorPicker
                    bind:selectedColorInx={input.value}
                    on:change={() => (isEditing = true)}
                />
            {:else}
                <input
                    type="text"
                    name={input.name}
                    placeholder={placeholderFor(input)}
                    class:input-error={!valid && input.error}
                    class="input input-bordered"
                    bind:value={input.value}
                    on:focus={() => (isEditing = true)}
                />
            {/if}
            {#if !valid && input.error}
                <div class="px-1 py-2  text-error text-xs">{input.error}</div>
            {/if}
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
