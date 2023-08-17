<script lang="ts">
    import { Eye, EyeOff } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { createEventDispatcher } from "svelte";

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
