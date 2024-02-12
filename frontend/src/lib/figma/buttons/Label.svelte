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
    import { _ } from "svelte-i18n";

    import type { LabelLabel } from "$lib/figma/types";
    import type { LabelColor } from "$lib/utils/colors";
    import {
        getLabelColorClass,
        getLabelColorFromIndex,
    } from "$lib/utils/colors";
    import { tw } from "$lib/utils/ui";

    export let label: LabelLabel;
    export let action: (() => void) | undefined;

    // TODO make undefined
    let labelColor: LabelColor | null;
    $: labelColor =
        label.kind === "applyLabel"
            ? null
            : getLabelColorFromIndex(label.label.color);

    let bgStyle: string;
    let hoverBgStyle: string;
    let textStyle: string;
    $: {
        if (labelColor) {
            bgStyle = getLabelColorClass("bg", labelColor);
            hoverBgStyle = getLabelColorClass("bgHover", labelColor);
            textStyle = getLabelColorClass("text", labelColor);
        } else {
            bgStyle = tw`bg-display`;
            hoverBgStyle = tw`hover:bg-background`;
            textStyle = tw`text-primary`;
        }
        // And then still remove hovering when it's disabled
        if (!action) {
            hoverBgStyle = "";
        }
    }
</script>

<!-- TODO no active state styling for this button -->
<button
    class="group rounded-2.5xl border border-dashed border-primary px-3 py-1 text-sm font-bold {bgStyle} {hoverBgStyle} {textStyle}"
    type="button"
    on:click={action}
    disabled={!action}
>
    {label.kind === "applyLabel" ? $_("label.apply-label") : label.label.name}
</button>
