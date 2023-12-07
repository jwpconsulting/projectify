<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";

    import type {
        ButtonAction,
        ButtonColor,
        ButtonSize,
        ButtonStyle,
    } from "$lib/funabashi/types";
    import { tw } from "$lib/utils/ui";

    export let style: ButtonStyle;
    export let color: ButtonColor;
    export let size: ButtonSize;
    export let label: string;
    export let action: ButtonAction;
    // XXX Hacky. Buttons have been inserted so far without caring for grow
    // or not. Grow depends on the outside being flex. This means this Button
    // is less "containerized" or "isolated".
    export let grow = true;

    $: innerColorStyle = {
        primary: {
            blue: tw`border-transparent bg-primary text-primary-content hover:bg-primary-hover active:bg-primary-pressed`,
            red: tw`border-transparent bg-destructive text-destructive-content hover:bg-destructive-hover active:bg-destructive-pressed`,
        },
        secondary: {
            blue: tw`border-secondary text-secondary-content hover:border-secondary-content-hover hover:bg-secondary-hover hover:text-secondary-content-hover active:border-border-secondary active:bg-secondary-pressed active:text-secondary-content-hover`,
            red: tw`border-destructive text-destructive hover:bg-destructive-secondary-hover hover:text-destructive-hover active:border-destructive active:bg-destructive-secondary-pressed active:text-destructive-pressed`,
        },
        tertiary: {
            blue: tw`text-tertiary-content hover:text-tertiary-content-hover active:bg-tertiary-pressed active:text-tertiary-content-hover`,
            red: tw`active:bg-destructive-secondary-presed text-destructive hover:text-destructive-hover active:text-destructive-hover`,
        },
    }[style.kind][color];
    $: innerSizeStyle = {
        "medium": tw`text-base`,
        "small": tw`text-sm`,
        "extra-small": tw`text-xs`,
    }[size];
    $: iconSizeStyle = {
        "medium": tw`h-6 w-6`,
        "small": tw`h-5 w-5`,
        "extra-small": tw`h-4 w-4`,
    }[size];

    $: outerGrowStyle = grow ? tw`w-full` : "";

    $: outerStyle = {
        primary: tw`${outerGrowStyle} group rounded-llg disabled:bg-disabled disabled:text-disabled-primary-content ${innerColorStyle} ${innerSizeStyle}`,
        secondary: tw`${outerGrowStyle} group rounded-llg disabled:bg-disabled disabled:text-disabled-primary-content ${innerColorStyle} ${innerSizeStyle}`,
        tertiary: tw`${outerGrowStyle} flex flex-row justify-center rounded-lg px-4 py-2 font-bold disabled:text-disabled-content ${innerColorStyle} ${innerSizeStyle}`,
    }[style.kind];

    $: innerStyle = {
        primary: tw`rounded-lg border px-4 py-2 font-bold`,
        secondary: tw`rounded-lg border px-4 py-2 font-bold`,
        tertiary: "",
    }[style.kind];

    // Outer element properties that button and submit share
    $: formProps =
        action.kind === "button" || action.kind === "submit"
            ? {
                  class: outerStyle,
                  disabled: action.disabled,
                  form: action.form,
              }
            : {};
</script>

{#if style.kind === "tertiary"}
    {#if action.kind === "a"}
        <a href={action.href} class={outerStyle} on:click={action.onInteract}>
            {#if style.icon && style.icon.position === "left"}
                <Icon
                    src={style.icon.icon}
                    theme="outline"
                    class={iconSizeStyle}
                />
            {/if}
            {label}
            {#if style.icon && style.icon.position === "right"}
                <Icon
                    src={style.icon.icon}
                    theme="outline"
                    class={iconSizeStyle}
                />
            {/if}
        </a>
    {:else if action.kind === "button"}
        <button
            on:click|preventDefault={action.action}
            {...formProps}
            type="button"
        >
            {#if style.icon && style.icon.position === "left"}
                <Icon
                    src={style.icon.icon}
                    theme="outline"
                    class={iconSizeStyle}
                />
            {/if}
            {label}
            {#if style.icon && style.icon.position === "right"}
                <Icon
                    src={style.icon.icon}
                    theme="outline"
                    class={iconSizeStyle}
                />
            {/if}
        </button>
    {:else}
        Not supported
    {/if}
{:else if action.kind === "a"}
    <a href={action.href} class={outerStyle} on:click={action.onInteract}>
        <div class={innerStyle}>
            {label}
        </div>
    </a>
{:else if action.kind === "button"}
    <button on:click|preventDefault={action.action} {...formProps}>
        <div class={innerStyle}>
            {label}
        </div>
    </button>
{:else}
    <button type="submit" {...formProps}>
        <div class={innerStyle}>
            {label}
        </div>
    </button>
{/if}
