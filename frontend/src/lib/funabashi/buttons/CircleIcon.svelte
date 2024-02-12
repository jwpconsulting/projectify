<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023-2024 JWP Consulting GK

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
        ChevronDown,
        ChevronUp,
        DotsHorizontal,
        Pencil,
        Trash,
        X,
    } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";

    import type {
        ButtonAction,
        CircleIconIcon,
        CircleIconSize,
    } from "$lib/funabashi/types";

    export let size: CircleIconSize;
    export let icon: CircleIconIcon;
    // TODO make required
    export let ariaLabel: string | undefined = undefined;

    export let action: ButtonAction & { kind: "a" | "button" };

    $: disabled = action.kind === "a" ? false : action.disabled ?? false;

    $: iconMapped = {
        ellipsis: DotsHorizontal,
        edit: Pencil,
        delete: Trash,
        up: ChevronUp,
        down: ChevronDown,
        close: X,
    }[icon];
    $: sizeMapped = {
        // TODO remove small
        small: "w-6 h-6 p-1",
        medium: "w-8 h-8 p-1.5",
    }[size];

    $: styleClasses = `${sizeMapped} rounded-full border border-transparent text-base-content hover:bg-secondary-hover active:bg-disabled-background`;
</script>

{#if action.kind === "button"}
    <button
        aria-label={ariaLabel}
        on:click|preventDefault|stopPropagation={action.action}
        {disabled}
        class="{styleClasses} disabled:bg-transparent disabled:text-transparent"
    >
        <Icon src={iconMapped} style="outline" />
    </button>
{:else if action.kind === "a"}
    <a href={action.href} class="block {styleClasses}" aria-label={ariaLabel}>
        <Icon src={iconMapped} style="outline" />
    </a>
{/if}
