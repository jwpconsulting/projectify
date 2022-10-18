<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Plus } from "@steeze-ui/heroicons";

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="group h-11 w-11 rounded-full border-2 border-transparent p-0.5 text-secondary-text focus:border-base-content focus:outline-none"
>
    <Icon
        src={Plus}
        theme="outline"
        class="rounded-full border-2 border-secondary-text group-hover:border-base-content group-hover:bg-secondary-hover group-hover:text-base-content group-focus:border-secondary-text group-active:border-transparent group-active:bg-primary group-active:text-display"
    />
</button>
