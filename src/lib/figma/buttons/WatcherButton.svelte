<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { EyeOff, Eye } from "@steeze-ui/heroicons";
    export let isActive: boolean;
    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    class="h-11 w-11 rounded-lg border border-transparent p-2.5 hover:bg-secondary focus:border-base-content"
    on:click={click}
>
    <Icon src={isActive ? Eye : EyeOff} theme="outline" />
</button>
