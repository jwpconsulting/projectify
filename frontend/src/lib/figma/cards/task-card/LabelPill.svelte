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
    import type { Label } from "$lib/types/workspace";
    import {
        getLabelColorClass,
        getLabelColorFromIndex,
    } from "$lib/utils/colors";

    export let label: Label;
    export let action: ((event: MouseEvent) => void) | undefined;
    let bgColorClass: string;
    let textColorClass: string;

    $: {
        const labelColor = getLabelColorFromIndex(label.color);
        if (labelColor) {
            bgColorClass = getLabelColorClass("bg", labelColor);
            textColorClass = getLabelColorClass("text", labelColor);
        }
    }
</script>

<button
    type="button"
    on:click|preventDefault={action}
    class="max-w-xs shrink-0 overflow-hidden text-ellipsis whitespace-nowrap rounded-full px-3 py-1 font-bold {bgColorClass} {textColorClass}"
>
    {label.name}
</button>
