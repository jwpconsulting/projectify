<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Minus } from "@steeze-ui/heroicons";

    export let disabled: boolean;

    const outerStyle = disabled ? "text-base-300" : "text-secondary-text";
    const innerStyle = disabled
        ? ""
        : "group-hover:text-base-content group-hover:bg-secondary group-focus:border-secondary-text";

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
