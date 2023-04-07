<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { X } from "@steeze-ui/heroicons";

    export let isActive: boolean;
    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="h-10 w-10 rounded-r-lg p-3 active:text-disabled-text enabled:hover:bg-secondary disabled:text-base-100"
    disabled={!isActive}
>
    <Icon src={X} theme="outline" />
</button>
