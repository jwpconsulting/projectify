<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { Label } from "$lib/types";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Check, Pencil, Trash } from "@steeze-ui/heroicons";
    import {
        getLabelColorFromIndex,
        getLabelColorClass,
    } from "$lib/utils/colors";
    export let label: Label | "all" | "none";
    export let onSelect: () => unknown;
    export let selected: boolean;
    export let editable = false;
    let borderColorClass = "";
    let bgColorClass = "";
    let hoverColorClass = "";
    let textColorClass = "";
    let textBgColorClass = "";
    let textHoverBgColorClass = "";
    $: {
        if (label === "all") {
            borderColorClass = "border-primary";
            bgColorClass = "bg-base-200";
            hoverColorClass = "hover:bg-secondary";
            textColorClass = "text-primary";
            textBgColorClass = "text-base-200";
            textHoverBgColorClass = "group-hover:text-secondary";
        } else if (label === "none") {
            borderColorClass = "border-task-update-text";
            bgColorClass = "bg-base-200";
            hoverColorClass = "hover:bg-base-300";
            textColorClass = "text-task-update-text";
            textBgColorClass = "text-base-200";
            textHoverBgColorClass = "group-hover:text-base-300";
        } else {
            const labelColor = getLabelColorFromIndex(label.color);
            if (labelColor) {
                borderColorClass = getLabelColorClass("border", labelColor);
                bgColorClass = getLabelColorClass("bg", labelColor);
                hoverColorClass = getLabelColorClass("bgHover", labelColor);
                textColorClass = getLabelColorClass("text", labelColor);
                textBgColorClass = getLabelColorClass("textBg", labelColor);
                textHoverBgColorClass = getLabelColorClass(
                    "textHoverBg",
                    labelColor
                );
            }
        }
    }
</script>

<div
    class="flex flex-row items-center justify-between px-5 py-2 hover:bg-base-200"
>
    <div class="flex flex-row items-center gap-2">
        <button class="p-0.5" on:click={onSelect}>
            <div
                class={`group h-6 items-center rounded-[20px] border-2 px-2 ${borderColorClass} ${bgColorClass} ${hoverColorClass}`}
            >
                <Icon
                    src={Check}
                    theme="outline"
                    class={`h-5 w-5 ${
                        selected
                            ? textColorClass
                            : `${textHoverBgColorClass} ${textBgColorClass}`
                    }`}
                />
            </div>
        </button>
        <div class="text-regular text-xs capitalize">
            {#if label === "all"}
                {$_("filter-label.all")}
            {:else if label === "none"}
                {$_("filter-label.none")}
            {:else}
                {label.name}
            {/if}
        </div>
    </div>
    <div class="flex flex-row items-center gap-2">
        {#if editable}
            <button class="p-1">
                <Icon src={Pencil} theme="outline" class="h-4 w-4" />
            </button>
            <button class="p-1">
                <Icon src={Trash} theme="outline" class="h-4 w-4" />
            </button>
        {/if}
    </div>
</div>
