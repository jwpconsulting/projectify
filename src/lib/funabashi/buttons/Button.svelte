<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
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

    $: colorStyle = {
        primary: {
            blue: tw`bg-primary text-primary-content hover:bg-primary-hover active:bg-primary-pressed`,
            red: tw`bg-destructive text-destructive-content hover:bg-destructive-hover active:bg-destructive-pressed`,
        },
        secondary: {
            blue: tw`text-secondary-content hover:bg-secondary-hover hover:text-secondary-content-hover active:bg-secondary-pressed active:text-secondary-content-hover`,
            red: tw`text-destructive hover:bg-destructive-secondary-hover hover:text-destructive-hover active:bg-destructive-secondary-pressed active:text-destructive-pressed`,
        },
        tertiary: {
            blue: tw`text-tertiary-content hover:text-tertiary-content-hover active:bg-tertiary-pressed active:text-tertiary-content-hover`,
            red: tw`active:bg-destructive-secondary-presed text-destructive hover:text-destructive-hover active:text-destructive-hover`,
        },
    }[style.kind][color];
    $: sizeStyle = {
        medium: tw`text-base`,
        small: tw`text-sm`,
    }[size];
    $: iconSizeStyle = {
        medium: tw`h-6 w-6`,
        small: tw`h-5 w-5`,
    }[size];

    $: outerGrowStyle = grow ? tw`w-full` : "";

    $: sharedStyle = tw`${outerGrowStyle} ${colorStyle} ${sizeStyle} flex min-w-max flex-row justify-center gap-2 rounded-lg px-4 py-2 font-bold`;
    $: composedStyle = {
        primary: tw`${sharedStyle} disabled:bg-disabled disabled:text-disabled-primary-content`,
        secondary: tw`${sharedStyle} disabled:bg-disabled disabled:text-disabled-primary-content`,
        tertiary: tw`${sharedStyle} disabled:bg-transparent disabled:text-disabled-content`,
    }[style.kind];

    // Outer element properties that button and submit share
    $: formProps =
        action.kind === "button" || action.kind === "submit"
            ? {
                  class: composedStyle,
                  disabled: action.disabled,
                  form: action.form,
              }
            : {};
</script>

{#if action.kind === "a"}
    <a href={action.href} class={composedStyle} on:click={action.onInteract}>
        {#if style.kind === "tertiary" && style.icon && style.icon.position === "left"}
            <Icon
                src={style.icon.icon}
                theme="outline"
                class={iconSizeStyle}
            />
        {/if}
        {label}
        {#if style.kind === "tertiary" && style.icon && style.icon.position === "right"}
            <Icon
                src={style.icon.icon}
                theme="outline"
                class={iconSizeStyle}
            />
        {/if}
    </a>
{:else if action.kind === "button"}
    <button on:click|preventDefault={action.action} {...formProps}>
        {#if style.kind === "tertiary" && style.icon && style.icon.position === "left"}
            <Icon
                src={style.icon.icon}
                theme="outline"
                class={iconSizeStyle}
            />
        {/if}
        {label}
        {#if style.kind === "tertiary" && style.icon && style.icon.position === "right"}
            <Icon
                src={style.icon.icon}
                theme="outline"
                class={iconSizeStyle}
            />
        {/if}
    </button>
{:else}
    <button type="submit" {...formProps}>
        {#if style.kind === "tertiary" && style.icon && style.icon.position === "left"}
            <Icon
                src={style.icon.icon}
                theme="outline"
                class={iconSizeStyle}
            />
        {/if}
        {label}
        {#if style.kind === "tertiary" && style.icon && style.icon.position === "right"}
            <Icon
                src={style.icon.icon}
                theme="outline"
                class={iconSizeStyle}
            />
        {/if}
    </button>
{/if}
