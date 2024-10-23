<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import {
        CheckCircle,
        DotsHorizontal,
        DotsVertical,
        Folder,
        LightBulb,
        Pencil,
        Plus,
        SwitchVertical,
        Tag,
        Trash,
        User,
        Users,
    } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";

    import type {
        ButtonAction,
        SquovalIcon,
        SquovalState,
    } from "$lib/funabashi/types";

    export let icon: SquovalIcon;
    $: src = {
        board: Folder,
        teamMember: User,
        label: Tag,
        bulk: CheckCircle,
        move: SwitchVertical,
        filterTeamMember: Users,
        delete: Trash,
        ellipsis: DotsHorizontal,
        plus: Plus,
        edit: Pencil,
        dotsVertical: DotsVertical,
        help: LightBulb,
    }[icon];
    // TODO active state should be renamed to enabled Justus 2023-03-07
    export let state: SquovalState;
    // XXX what is active again?
    export let active = false;

    export let action: ButtonAction & { kind: "button" | "a" };
    export let ariaLabel: string;

    const style =
        "focus:base-content relative h-8 w-8 rounded-lg border border-transparent p-1 focus:border-base-content focus:outline-none active:text-display enabled:hover:bg-secondary-hover enabled:active:bg-primary";
    const activeStyle =
        "border-base absolute left-5 top-1 h-2 w-2 rounded-full border bg-primary";
</script>

<!-- terrible hack. Ideally we don't support this being an anchor at all -->
{#if action.kind === "button"}
    <button
        aria-label={ariaLabel}
        on:click={action.action}
        class={style}
        class:text-base-content={state === "active"}
        class:invisible={state === "inactive"}
        class:text-secondary-text={state === "disabled"}
        disabled={state !== "active"}
    >
        {#if active}
            <div class={activeStyle} />
        {/if}
        <Icon {src} theme="outline" />
    </button>
{:else}
    <a
        aria-label={ariaLabel}
        href={action.href}
        on:click={action.onInteract}
        class={style}
        class:block={action.kind === "a"}
    >
        {#if active}
            <div class={activeStyle} />
        {/if}
        <Icon {src} theme="outline" />
    </a>
{/if}
