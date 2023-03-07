<script lang="ts">
    import { _ } from "svelte-i18n";
    import { createEventDispatcher } from "svelte";
    import type { LabelColor } from "$lib/utils/colors";
    import {
        getLabelColorFromIndex,
        getLabelColorClass,
    } from "$lib/utils/colors";
    import type { LabelLabel } from "$lib/figma/types";

    export let label: LabelLabel;

    let labelColor: LabelColor | null;
    $: labelColor =
        label.kind === "applyLabel"
            ? null
            : getLabelColorFromIndex(label.label.color);

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
        innerStyle = `flex flex-row items-center justify-center rounded-2.5xl border px-3 py-1 text-xxs font-bold capitalize ${innerBorderStyle} ${bgStyle} ${hoverBgStyle} ${textStyle}`;
    }

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button class={outerStyle} on:click={click}>
    <div class={innerStyle}>
        {label.kind === "applyLabel"
            ? $_("label.apply-label")
            : label.label.name}
    </div>
</button>
