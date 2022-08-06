<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Check } from "@steeze-ui/heroicons";
    import { createEventDispatcher } from "svelte";
    import {
        getLabelColorFromIndex,
        getLabelColorClass,
    } from "$lib/utils/colors";
    import type { SelectLabel } from "$lib/figma/types";

    export let label: SelectLabel;
    export let active: boolean;

    let outerStyle: string;
    let innerStyle: string;
    $: {
        if (label.kind == "allLabels") {
            outerStyle =
                "bg-background border-primary hover:bg-secondary-hover text-primary";
        } else if (label.kind == "noLabel") {
            outerStyle =
                "bg-background border-utility hover:bg-border text-utility";
        } else {
            let color = getLabelColorFromIndex(label.label.color);
            if (!color) {
                throw new Error("Expected color");
            }
            outerStyle = `${getLabelColorClass(
                "bg",
                color
            )} ${getLabelColorClass("border", color)} ${getLabelColorClass(
                "bgHover",
                color
            )} ${getLabelColorClass("text", color)}`;
        }
    }

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class={`flex h-6 w-10 flex-row items-center justify-center rounded-2.5xl border border-2 px-2.5 py-0.5 ${outerStyle}`}
>
    <Icon
        src={Check}
        theme="outline"
        class={`${active ? "visible" : "invisible"} ${innerStyle}`}
    />
</button>
