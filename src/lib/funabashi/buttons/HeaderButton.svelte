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
    import type { ButtonAction } from "$lib/funabashi/types";

    export let label: string;
    export let action: ButtonAction;
    const buttonClass =
        "text-base-content flex flex-row items-center gap-2 rounded-lg p-2 hover:text-primary focus:outline-none focus:ring-1 focus:ring-border-focus focus:ring-offset-2 active:text-primary";
</script>

{#if action.kind === "button"}
    <button
        on:click={action.action}
        on:keydown={action.action}
        class={buttonClass}
    >
        <div class="text-base font-bold">
            {label}
        </div>
    </button>
{:else if action.kind === "a"}
    <!-- we just ignore the dropdown case for now -->
    <a href={action.href} class={buttonClass} on:click={action.onInteract}>
        <div class="text-base font-bold">
            {label}
        </div>
    </a>
{/if}
