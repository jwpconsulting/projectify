<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
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
