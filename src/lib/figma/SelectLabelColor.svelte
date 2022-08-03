<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Check } from "@steeze-ui/heroicons";
    import { createEventDispatcher } from "svelte";
    import { getLabelColorClass } from "$lib/utils/colors";
    import type { LabelColor } from "$lib/utils/colors";

    export let color: LabelColor;
    export let active: boolean;

    $: outerStyle = `${getLabelColorClass("bg", color)} ${getLabelColorClass(
        "border",
        color
    )} ${getLabelColorClass("bgHover", color)}`;
    $: innerStyle = ``;

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
