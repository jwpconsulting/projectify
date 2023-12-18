<script lang="ts">
    import { Check } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";

    import type { SelectLabel } from "$lib/figma/types";
    import {
        getLabelColorClass,
        getLabelColorFromIndex,
        type LabelColor,
    } from "$lib/utils/colors";

    export let label:
        | SelectLabel
        | { kind: "createLabel"; labelColor: LabelColor };
    export let checked: boolean;
    // This should be required
    export let name: string | undefined = undefined;

    // think about whether we really need these
    export let onCheck: () => void;
    export let onUncheck: () => void;

    function onChange() {
        if (checked) {
            onCheck();
        } else {
            onUncheck();
        }
    }

    let outerStyle: string;
    let outerStyleComputed: string;
    $: {
        if (label.kind == "allLabels") {
            outerStyle =
                "bg-background border-primary group-hover:bg-secondary-hover hover:bg-secondary-hover text-primary";
        } else if (label.kind == "noLabel") {
            outerStyle =
                "bg-background border-utility group-hover:bg-border hover:bg-border text-utility";
        } else {
            const color =
                label.kind === "createLabel"
                    ? label.labelColor
                    : getLabelColorFromIndex(label.label.color);
            if (!color) {
                throw new Error("Expected color");
            }
            outerStyle = `${getLabelColorClass(
                "bg",
                color,
            )} ${getLabelColorClass("border", color)} ${getLabelColorClass(
                "bgHover",
                color,
            )} ${getLabelColorClass("text", color)}`;
        }
        outerStyleComputed = `flex h-6 w-10 flex-row items-center justify-center rounded-2.5xl border border-2 px-2.5 ${outerStyle}`;
    }
</script>

<div class="group relative h-7 w-11 p-0.5">
    <div class={outerStyleComputed}>
        <div class:visible={checked} class:invisible={!checked}>
            <Icon src={Check} theme="outline" />
        </div>
    </div>
    <input
        type="checkbox"
        bind:checked
        on:change={onChange}
        on:click|stopPropagation
        {name}
        class="absolute left-0 top-0 h-7 w-11 appearance-none rounded-1.5xl border border-transparent focus:border-base-content focus:outline-none"
    />
</div>
