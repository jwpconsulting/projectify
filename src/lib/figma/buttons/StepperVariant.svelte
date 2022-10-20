<script lang="ts">
    import type {
        StepperPosition,
        StepperActiveState,
    } from "$lib/figma/types";
    import { createEventDispatcher } from "svelte";

    export let position: StepperPosition;
    export let state: StepperActiveState;

    const dispatch = createEventDispatcher();

    function click() {
        dispatch("click");
    }
</script>

<button on:click={click} class="group flex flex-row items-center">
    <div
        class="h-4 w-4 rounded-full bg-base-300 group-active:bg-primary-hover"
        class:bg-primary-hover={state !== "inactive"}
    />
    {#if position !== "last"}
        <div
            class={`h-1 w-5 bg-base-300`}
            class:bg-primary-hover={state === "next"}
        />
    {/if}
</button>
