<script lang="ts">
    import { _ } from "svelte-i18n";

    import type { LabelLabel } from "$lib/figma/types";
    import type { LabelColor } from "$lib/utils/colors";
    import {
        getLabelColorClass,
        getLabelColorFromIndex,
    } from "$lib/utils/colors";

    export let label: LabelLabel;
    export let action: (() => void) | undefined;

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
        // And then still remove hovering when it's disabled
        if (!action) {
            hoverBgStyle = "";
        }
        outerStyle = `group rounded-2.5xl border p-px focus:outline-none ${outerBorderStyle}`;
        innerStyle = `flex flex-row items-center justify-center rounded-2.5xl border px-3 py-1 text-sm font-bold ${innerBorderStyle} ${bgStyle} ${hoverBgStyle} ${textStyle}`;
    }
</script>

<button class={outerStyle} type="button" on:click={action} disabled={!action}>
    <div class={innerStyle}>
        {label.kind === "applyLabel"
            ? $_("label.apply-label")
            : label.label.name}
    </div>
</button>
