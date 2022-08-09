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
    export let contained: boolean = false;

    let outerStyle: string;
    let outerStyleComputed: string;
    let innerStyle: string;
    $: {
        if (label.kind == "allLabels") {
            outerStyle =
                "bg-background border-primary group-hover:bg-secondary-hover hover:bg-secondary-hover text-primary";
        } else if (label.kind == "noLabel") {
            outerStyle =
                "bg-background border-utility group-hover:bg-border hover:bg-border text-utility";
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
        outerStyleComputed = `flex h-6 w-10 flex-row items-center justify-center rounded-2.5xl border border-2 px-2.5 py-0.5 ${outerStyle}`;
    }

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<svelte:element
    this={contained ? "div" : "button"}
    on:click={contained ? undefined : click}
    class={outerStyleComputed}
>
    <Icon
        src={Check}
        theme="outline"
        class={`${active ? "visible" : "invisible"} ${innerStyle}`}
    />
</svelte:element>
