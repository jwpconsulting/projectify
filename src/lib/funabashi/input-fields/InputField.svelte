<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Search, X } from "@steeze-ui/heroicons";
    import type { InputFieldAnchor, InputFieldStyle } from "$lib/figma/types";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";

    // TODO make border customizable (e.g. in TaskFormFields)
    export let value: string | null = null;
    export let placeholder: string;
    export let style: InputFieldStyle;
    export let name: string;
    export let label: string | null = null;
    export let anchorTop: InputFieldAnchor | null = null;
    export let anchorBottom: InputFieldAnchor | null = null;
    export let required = false;

    const inputStyle =
        "text-regular placeholder:text-task-update-text peer relative top-0 left-0 z-10 h-full w-full rounded-lg border border-border pr-8 text-xs focus:outline-none";

    function clear() {
        value = "";
    }
</script>

<div class="flex flex-col items-start">
    <div class="flex w-full flex-row items-center justify-between">
        {#if label}
            <label
                for={name}
                class="p-2 text-xs font-bold text-base-content first-letter:uppercase"
            >
                {label}
            </label>
        {/if}
        {#if anchorTop}
            <Anchor
                href={anchorTop.href}
                label={anchorTop.label}
                size="extraSmall"
            />
        {/if}
    </div>
    <div class="relative isolate h-12 w-full p-1">
        {#if style.kind === "search"}
            <input
                type="text"
                class={`${inputStyle} pl-8`}
                {name}
                bind:value
                {placeholder}
                {required}
            />
        {:else if style.kind === "subTask"}
            <input
                type="text"
                class={`${inputStyle} pl-2`}
                {name}
                bind:value
                {placeholder}
                {required}
            />
        {:else if style.kind === "field"}
            {#if style.inputType === "text"}
                <input
                    type="text"
                    class={`${inputStyle} pl-2`}
                    {name}
                    bind:value
                    {placeholder}
                    {required}
                />
            {:else if style.inputType === "email"}
                <input
                    type="email"
                    class={`${inputStyle} pl-2`}
                    {name}
                    bind:value
                    {placeholder}
                    {required}
                />
            {:else if style.inputType === "password"}
                <input
                    type="password"
                    class={`${inputStyle} pl-2`}
                    {name}
                    bind:value
                    {placeholder}
                    {required}
                />
            {/if}
        {/if}
        <div
            class="absolute left-0 top-0 z-0 h-full w-full rounded-xl border-2 border-transparent peer-focus:border-border"
        />
        {#if style.kind === "search"}
            <div
                class="absolute left-0.5 top-0.5 z-20 flex flex-row items-center justify-between"
            >
                <div class="flex flex-row gap-2.5 p-3">
                    <Icon
                        src={Search}
                        theme="outline"
                        class="h-4 w-4 text-base-content"
                    />
                </div>
            </div>
        {/if}
        {#if value}
            <button
                class="absolute right-0.5 top-0.5 z-20 flex flex-row gap-2.5 p-3"
                on:click|preventDefault={clear}
                type="button"
            >
                <Icon
                    src={X}
                    theme="outline"
                    class="h-4 w-4 text-base-content"
                />
            </button>
        {/if}
    </div>
    <div class="flex w-full flex-row items-center justify-between gap-1">
        <div />
        {#if anchorBottom}
            <Anchor
                href={anchorBottom.href}
                label={anchorBottom.label}
                size="extraSmall"
            />
        {/if}
    </div>
</div>
