<script lang="ts">
    import { Search, X } from "@steeze-ui/heroicons";
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

    import { browser } from "$app/environment";

    // TODO make border customizable (e.g. in TaskFormFields)
    export let value: string | undefined = undefined;
    export let placeholder: string;
    export let style: InputFieldStyle;
    export let name: string;
    /**
     * Designate the id for this input element, falls back to name
     */
    export let id: string | undefined = undefined;
    // TODO
    // export let label: string | undefined = undefined;
    export let label: string | null = null;
    // TODO
    // export let anchorTop: InputFieldAnchor | undefined = undefined;
    export let anchorTop: InputFieldAnchor | null = null;
    // TODO
    // export let anchorBottom: InputFieldAnchor | undefined = undefined;
    export let anchorBottom: InputFieldAnchor | null = null;
    export let required = false;
    export let readonly = false;
    export let onClick: (() => void) | undefined = undefined;
    export let validation: InputFieldValidation | undefined = undefined;

    let pikadayAnchor: HTMLElement | undefined = undefined;
    let pikaday: typeof Pikaday | undefined = undefined;
    let datePicker: Pikaday | undefined = undefined;

    $: id = id ?? name;

    // Possibly we can just have two onMount calls here, but I couldn't read
    // from the svelte docs whether that is explicitly supported or not.
    onMount(() => {
        if (!browser) {
            return;
        }
        // We have no further business if no date picker
        if (!(style.kind === "field" && style.inputType === "date")) {
            return;
        }

        import("pikaday")
            .then((mod) => {
                pikaday = mod.default;
            })
            .catch(console.error);
        return () => {
            if (!datePicker) {
                return;
            }
            datePicker.destroy();
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

    const inputStyle =
        "text-regular placeholder:text-task-update-text peer relative top-0 left-0 z-10 h-full w-full rounded-lg border border-border pr-8 text-xs focus:outline-none";

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
</script>

<div class="flex flex-col items-start gap-2">
    {#if label !== null || anchorTop !== null}
        <div
            class="flex w-full flex-row items-center"
            class:justify-between={label}
            class:justify-end={!label}
        >
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
                    size="small"
                />
            {/if}
        </div>
    {/if}
    <div class="relative isolate h-12 w-full p-1">
        {#if style.kind === "search"}
            <input
                type="text"
                class={`${inputStyle} pl-8`}
                {...inputProps}
                bind:value
                on:click={onClick}
            />
        {:else if style.kind === "field"}
            {#if style.inputType === "text"}
                <input
                    type="text"
                    class={`${inputStyle} pl-2`}
                    {...inputProps}
                    bind:value
                    on:click={onClick}
                />
            {:else if style.inputType === "password"}
                <input
                    type="password"
                    class={`${inputStyle} pl-2`}
                    {...inputProps}
                    bind:value
                    on:click={onClick}
                />
            {:else if style.inputType === "email"}
                <input
                    type="email"
                    class={`${inputStyle} pl-2`}
                    {...inputProps}
                    bind:value
                    on:click={onClick}
                />
            {:else if style.inputType === "date"}
                <input
                    type="text"
                    class={`${inputStyle} pl-2`}
                    {...inputProps}
                    bind:value
                    on:click={onClick}
                    bind:this={pikadayAnchor}
                />
            {/if}
        {/if}
        <div
            class="absolute left-0 top-0 z-0 h-full w-full rounded-xl border-2 border-transparent peer-focus:border-border"
        />
        {#if style.kind === "search"}
            <!-- XXX not centered horizontally... -->
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
        {#if value && !readonly}
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
    {#if anchorBottom !== null || validation !== undefined}
        <div
            class="flex w-full flex-row items-end justify-end gap-1 px-1"
            class:justify-end={anchorBottom && !validation}
            class:justify-between={anchorBottom && validation}
        >
            {#if validation}
                <p
                    class="text-s"
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
                <Anchor
                    href={anchorBottom.href}
                    label={anchorBottom.label}
                    size="small"
                />
            {/if}
        </div>
    {/if}
</div>
