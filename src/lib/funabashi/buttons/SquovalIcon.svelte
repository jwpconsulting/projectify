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
        workspaceUser: User,
        label: Tag,
        bulk: CheckCircle,
        move: SwitchVertical,
        filterWorkspaceUser: Users,
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

    const style =
        "focus:base-content relative h-8 w-8 rounded-lg border border-transparent p-1 focus:border-base-content focus:outline-none active:text-display enabled:hover:bg-secondary-hover enabled:active:bg-primary";
    const activeStyle =
        "border-base absolute left-5 top-1 h-2 w-2 rounded-full border bg-primary";
</script>

<!-- terrible hack. Ideally we don't support this being an anchor at all -->
{#if action.kind === "button"}
    <button
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
