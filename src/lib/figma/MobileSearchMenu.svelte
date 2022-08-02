<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Search } from "@steeze-ui/heroicons";
    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="h-11 w-11 rounded-lg border border-transparent p-2.5 hover:bg-secondary focus:border-base-content focus:outline-none"
>
    <Icon src={Search} theme="outline" />
</button>
