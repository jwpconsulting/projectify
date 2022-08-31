<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Folder } from "@steeze-ui/heroicons";
    import type { BoardButtonState } from "$lib/figma/types";

    export let state: BoardButtonState;

    $: style = {
        inactive: "invisible",
        disabled: "text-secondary-text",
        active: "text-base-content hover:bg-secondary-hover active:bg-primary active:text-base-100 focus:outline-none focus:border-base-content",
    }[state];
    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class={`h-6 w-6 rounded-md border border-transparent p-1 focus:border-base-content focus:outline-none ${style}`}
    disabled={state !== "active"}
>
    <Icon src={Folder} theme="outline" />
</button>
