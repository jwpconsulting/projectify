<script lang="ts">
    import { Minus } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { createEventDispatcher } from "svelte";

    export let disabled: boolean;

    $: outerStyle = disabled
        ? "text-disabled-background"
        : "text-secondary-text";
    $: innerStyle = disabled
        ? "border-disabled-background"
        : "border-secondary-text group-hover:text-base-content group-hover:border-base-content group-hover:bg-secondary-hover group-active:bg-primary group-active:text-display group-active:border-display group-focus:border-secondary-text";

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class={`group h-11 w-11 rounded-full border-2 border-transparent p-0.5 focus:border-base-content focus:outline-none ${outerStyle}`}
    {disabled}
>
    <Icon
        src={Minus}
        theme="outline"
        class={`rounded-full border-2 ${innerStyle}`}
    />
</button>
