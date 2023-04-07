<script lang="ts">
    import IconClose from "$lib/components/icons/icon-close.svelte";
    import type { Label } from "$lib/types/workspace";
    import {
        getLabelColorClass,
        getLabelColorFromIndex,
    } from "$lib/utils/colors";

    export let label: Label;
    export let deleteIcon = false;
    const labelColor = getLabelColorFromIndex(label.color);
    let bgColorClass: string;
    let textColorClass: string;
    if (labelColor) {
        bgColorClass = getLabelColorClass("bg", labelColor);
        textColorClass = getLabelColorClass("text", labelColor);
    }
</script>

<div class="p-0.5">
    <div class="rounded-xl p-0.5">
        <div
            class={`label max-w-xs whitespace-nowrap rounded-full px-3 py-1 text-xxs font-bold ${bgColorClass} ${textColorClass}`}
        >
            <span class="nowrap-ellipsis">{label.name}</span>
            {#if deleteIcon}
                <div
                    class="relative mr-[-8px] ml-2 flex h-4 w-4 items-center justify-center rounded-full bg-current"
                >
                    <div class="absolute top-[-1px] h-3 w-3 text-[#fff]">
                        <IconClose />
                    </div>
                </div>
            {/if}
        </div>
    </div>
</div>
