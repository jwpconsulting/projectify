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
