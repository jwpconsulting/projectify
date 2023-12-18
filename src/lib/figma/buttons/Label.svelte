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

    let labelColor: LabelColor | null;
    $: labelColor =
        label.kind === "applyLabel"
            ? null
            : getLabelColorFromIndex(label.label.color);

    let innerBorderStyle: string;
    let bgStyle: string;
    let hoverBgStyle: string;
    let textStyle: string;
    $: {
        if (labelColor) {
            innerBorderStyle = tw``;
            bgStyle = getLabelColorClass("bg", labelColor);
            hoverBgStyle = getLabelColorClass("bgHover", labelColor);
            textStyle = getLabelColorClass("text", labelColor);
        } else {
            innerBorderStyle = tw`border-dashed border-primary`;
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

<button
    class="group rounded-2.5xl border px-3 py-1 text-sm font-bold {innerBorderStyle} {bgStyle} {hoverBgStyle} {textStyle}"
    type="button"
    on:click={action}
    disabled={!action}
>
    {label.kind === "applyLabel" ? $_("label.apply-label") : label.label.name}
</button>
