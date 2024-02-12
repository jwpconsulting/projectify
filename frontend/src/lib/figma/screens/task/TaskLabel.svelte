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
    import LabelC from "$lib/figma/buttons/Label.svelte";
    import type { Label } from "$lib/types/workspace";

    export let onInteract: ((anchor: HTMLElement) => void) | undefined =
        undefined;
    export let readonly = false;

    export let labels: Label[];

    let btnRef: HTMLElement;
</script>

<div class="flex flex-row flex-wrap items-center gap-x-1 gap-y-2">
    {#each labels as label}
        <div class="shrink-0">
            <LabelC
                label={{ kind: "label", label }}
                action={onInteract ? onInteract.bind(null, btnRef) : undefined}
            />
        </div>
    {/each}
    {#if !readonly && onInteract}
        <div class="shrink-0" bind:this={btnRef}>
            <LabelC
                label={{ kind: "applyLabel" }}
                action={onInteract.bind(null, btnRef)}
            />
        </div>
    {/if}
</div>
