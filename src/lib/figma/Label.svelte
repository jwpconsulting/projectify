<script lang="ts">
    import { _ } from "svelte-i18n";
    import { createEventDispatcher } from "svelte";
    import type { Label } from "$lib/types";
    import type { LabelColor } from "$lib/utils/colors";
    import {
        getLabelColorFromIndex,
        getLabelColorClass,
    } from "$lib/utils/colors";

    export let label: "applyLabel" | Label;

    let labelColor: LabelColor | null;
    $: labelColor =
        label === "applyLabel" ? null : getLabelColorFromIndex(label.color);

    let outerBorderStyle: string;
    let innerBorderStyle: string;
    let bgStyle: string;
    let hoverBgStyle: string;
    let textStyle: string;
    let outerStyle: string;
    let innerStyle: string;
    $: {
        if (labelColor) {
            outerBorderStyle = `border-transparent ${getLabelColorClass(
                "focusBorder",
                labelColor
            )}`;
            innerBorderStyle = "border-transparent";
            bgStyle = getLabelColorClass("bg", labelColor);
            hoverBgStyle = getLabelColorClass("bgHover", labelColor);
            textStyle = getLabelColorClass("text", labelColor);
        } else {
            outerBorderStyle = "border-transparent focus:border-primary";
            innerBorderStyle = "border-dashed border-primary";
            bgStyle = "bg-display";
            hoverBgStyle = "hover:bg-background";
            textStyle = "text-primary";
        }
        outerStyle = `group rounded-2.5xl border p-px focus:outline-none ${outerBorderStyle}`;
        innerStyle = `flex flex-row items-center justify-center rounded-2.5xl border px-3 py-px text-xxs font-bold capitalize ${innerBorderStyle} ${bgStyle} ${hoverBgStyle} ${textStyle}`;
    }

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button class={outerStyle} on:click={click}>
    <div class={innerStyle}>
        {label === "applyLabel" ? $_("label.apply-label") : label.name}
    </div>
</button>
