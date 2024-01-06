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

<div class="p-0.5">
    <div class="rounded-xl p-0.5">
        <div
            class={`label max-w-xs whitespace-nowrap rounded-full px-3 py-1 text-sm font-bold ${bgColorClass} ${textColorClass}`}
        >
            <span class="nowrap-ellipsis">{label.name}</span>
        </div>
    </div>
</div>
