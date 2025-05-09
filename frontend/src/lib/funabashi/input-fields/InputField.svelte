<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { Pencil, X } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { parseISO } from "date-fns";
    import type Pikaday from "pikaday";
    import type { PikadayOptions } from "pikaday";
    import { onMount } from "svelte";

    import type {
        InputFieldAnchor,
        InputFieldStyle,
        InputFieldValidation,
    } from "$lib/funabashi/types";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { formatIsoDate } from "$lib/utils/date";
    import { tw } from "$lib/utils/ui";

    // TODO make border customizable (e.g. in TaskFormFields)
    export let value: string | undefined | null = undefined;
    export let placeholder: string;
    export let style: InputFieldStyle;
    export let name: string;
    /**
     * Designate the id for this input element, falls back to name
     * XXX not guaranteed to be unique - problematic!
     */
    export let id: string | undefined = undefined;
    export let label: string | undefined;
    export let anchorTop: InputFieldAnchor | undefined = undefined;
    export let anchorBottom: InputFieldAnchor | undefined = undefined;
    export let required = false;
    export let readonly = false;
    export let onClick: (() => void) | undefined = undefined;
    export let onEnter: (() => void) | undefined = undefined;
    export let validation: InputFieldValidation | undefined = undefined;

    let pikadayAnchor: HTMLElement | undefined = undefined;
    let pikaday: typeof Pikaday | undefined = undefined;
    let datePicker: Pikaday | undefined = undefined;

    // XXX not guaranteed to be unique
    $: id = id ?? name;
    // Should we show a clear button - at all?
    export let showClearButton = false;
    $: hideClearButton = !showClearButton || value === undefined || readonly;

    $: {
        if (onEnter !== undefined && style.inputType !== "text") {
            console.warn(
                "At this moment, onEnter is only supported for text until a use case for other input types support onEnter as well is found.",
            );
        }
    }

    onMount(() => {
        if (style.inputType === "date") {
            import("pikaday")
                .then((mod) => {
                    pikaday = mod.default;
                })
                .catch((error: unknown) => console.error(error));
        }
    });
    onMount(() => {
        return () => {
            if (datePicker) {
                datePicker.destroy();
            }
        };
    });

    const getPikadayOptions = (field: HTMLElement): PikadayOptions => {
        return {
            field,
            toString(date: Date, _format: string): string {
                return formatIsoDate(date);
            },
            parse(dateString: string, _format: string): Date {
                return parseISO(dateString);
            },
            onSelect(date: Date) {
                // The two way binding falls apart when pikaday piks a date
                // for us. To mitigate, we set value here.
                value = formatIsoDate(date);
            },
        };
    };

    $: {
        // TODO find out if we should avoid showing this on mobile
        if (pikaday && pikadayAnchor && !readonly) {
            datePicker = new pikaday(getPikadayOptions(pikadayAnchor));
        } else if (datePicker && readonly) {
            datePicker.destroy();
        }
    }

    const inputStyle = tw`placeholder:text-task-update-text peer h-full w-full rounded-lg border border-border px-2 py-2`;

    function clear() {
        value = undefined;
    }

    $: inputProps = {
        id,
        name,
        placeholder,
        required,
        readonly: readonly || undefined,
    };

    function onKeydown(event: KeyboardEvent) {
        if (event.key === "Enter" && onEnter !== undefined) {
            event.preventDefault();
        }
    }

    function onKeyup(event: KeyboardEvent) {
        if (event.key === "Enter" && onEnter !== undefined) {
            onEnter();
        }
    }
</script>

<div class="flex flex-col items-start gap-2">
    {#if label !== undefined || anchorTop !== undefined}
        <div
            class="flex w-full flex-row items-center"
            class:justify-between={label}
            class:justify-end={!label}
        >
            {#if label}
                <label
                    for={id}
                    class="font-bold text-base-content first-letter:uppercase"
                >
                    {label}
                </label>
            {/if}
            {#if anchorTop}
                <Anchor href={anchorTop.href} label={anchorTop.label} />
            {/if}
        </div>
    {/if}
    <div class="flex w-full flex-row items-center gap-2">
        {#if $$slots.left}
            <slot name="left" />
        {/if}
        {#if style.inputType === "text"}
            <input
                type="text"
                class={inputStyle}
                {...inputProps}
                bind:value
                on:keydown={onKeydown}
                on:keyup={onKeyup}
            />
        {:else if style.inputType === "password"}
            <input
                type="password"
                class={inputStyle}
                {...inputProps}
                bind:value
            />
        {:else if style.inputType === "search"}
            <input
                type="search"
                class={inputStyle}
                {...inputProps}
                bind:value
            />
        {:else if style.inputType === "email"}
            <input
                type="email"
                class={inputStyle}
                {...inputProps}
                bind:value
            />
        {:else if style.inputType === "date"}
            <input
                type="text"
                class={inputStyle}
                {...inputProps}
                bind:value
                bind:this={pikadayAnchor}
            />
        {:else if style.inputType === "numeric"}
            <input
                type="number"
                inputmode="numeric"
                class={inputStyle}
                {...inputProps}
                bind:value
                bind:this={pikadayAnchor}
                min={style.min}
                max={style.max}
            />
        {/if}
        {#if readonly && onClick}
            <button
                class="flex flex-row"
                on:click|preventDefault={onClick}
                type="button"
            >
                <Icon src={Pencil} theme="outline" class="h-4 w-4" />
            </button>
        {/if}
        {#if showClearButton}
            <button
                class="flex flex-row"
                on:click|preventDefault={clear}
                type="button"
                disabled={hideClearButton}
                class:invisible={hideClearButton}
            >
                <Icon src={X} theme="outline" class="h-4 w-4" />
            </button>
        {/if}
    </div>
    {#if anchorBottom !== undefined || validation !== undefined}
        <div
            class="flex w-full flex-row items-end justify-end gap-1 px-1"
            class:justify-end={anchorBottom && !validation}
            class:justify-between={anchorBottom && validation}
        >
            {#if validation}
                <p
                    class:text-success={validation.ok}
                    class:text-error={!validation.ok}
                >
                    {#if validation.ok}
                        {validation.result}
                    {:else}
                        {validation.error}
                    {/if}
                </p>
            {/if}
            {#if anchorBottom}
                <Anchor href={anchorBottom.href} label={anchorBottom.label} />
            {/if}
        </div>
    {/if}
</div>
