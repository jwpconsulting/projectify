<script lang="ts">
    import { offsetLimitPagination } from "@apollo/client/utilities";

    import { getContext } from "svelte";
    import { _ } from "svelte-i18n";
    import ColorPicker from "./colorPicker.svelte";
    import InputDatePicker from "./inputDatePicker.svelte";

    export let title;
    export let subtitle = null;
    export let cancelLabel = $_("Cancel");
    export let confirmLabel = $_("Confirm");
    export let confirmColor = "primary";

    export let inputs: {
        name?: string;
        label?: string;
        type?: string;
        value?: any;
        error?: string;
        placeholder?: string;
        selectOptions?: { label: string; value: any }[];
        validation?: {
            required?: boolean;
            validator?: (
                value: any,
                data: any
            ) => {
                error?: boolean;
                message?: string;
            };
            // Todo:
            // min?: number;
            // max?: number;
            // minLength?: number;
            // maxLength?: number;
            // pattern?: string;
        };
    }[] = [];
    let isEditing = false;

    const modal = getContext<any>("modal");
    let data = modal.getData();

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
        valid = true;

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

            if (field.validation?.validator) {
                const res = field.validation?.validator(field.value, data);

                if (res?.error) {
                    valid = false;
                    field.error = res.message;
                }
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
        <h1 class="pb-4 text-center text-3xl font-bold">{title}</h1>
        {#if subtitle}
            <div class="text-center">{subtitle}</div>
        {/if}
        <div class="pt-4">
            <slot />
        </div>
    </div>
    {#each inputs as input, inx}
        <div class="form-control w-full">
            <label for={input.name} class="label label-text uppercase"
                >{input.label}</label
            >
            {#if input.type == "colorPicker"}
                <ColorPicker
                    bind:selectedColorInx={input.value}
                    on:change={() => (isEditing = true)}
                />
            {:else if input.type == "datePicker"}
                <InputDatePicker bind:input bind:isEditing />
            {:else if input.type == "select"}
                <select
                    class:select-error={!valid && input.error}
                    class="select select-bordered w-full"
                    on:change={(e) => {
                        isEditing = true;
                        input.value = e.target["value"];
                    }}
                >
                    <option disabled selected={!input.value}
                        >{input.placeholder}</option
                    >
                    {#each input.selectOptions as option}
                        <option
                            selected={input.value == option.value}
                            value={option.value}>{option.label}</option
                        >
                    {/each}

                    {input.value}
                </select>
            {:else}
                <input
                    autofocus={inx == 0}
                    type="text"
                    name={input.name}
                    placeholder={placeholderFor(input)}
                    class:input-error={!valid && input.error}
                    class="input input-bordered"
                    on:keypress={(e) => {
                        isEditing = true;
                        if (e.key == "Enter") {
                            confirm();
                        }
                    }}
                    bind:value={input.value}
                    on:focus={() => (isEditing = true)}
                />
            {/if}
            {#if !valid && input.error}
                <div class="px-1 py-2  text-xs text-error">{input.error}</div>
            {/if}
        </div>
    {/each}
    <div class="flex w-full space-x-2 pt-9">
        <button
            class="btn btn-outline btn-primary grow"
            on:click|preventDefault={cancel}>{cancelLabel}</button
        >
        <button
            class:btn-primary={confirmColor == "primary"}
            class:btn-accent={confirmColor == "accent"}
            class="btn grow"
            on:click|preventDefault={confirm}>{confirmLabel}</button
        >
    </div>
</div>
