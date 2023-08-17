<script lang="ts">
    import { CheckCircle } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { createEventDispatcher } from "svelte";

    export let isRead: boolean;
    const dispatch = createEventDispatcher();
    $: classes = isRead
        ? "text-transparent"
        : "bg-secondary text-secondary hover:bg-base-100 hover:text-secondary-text";
    function click() {
        dispatch("click");
    }
</script>

{!isRead}
<button
    on:click={click}
    class={`h-5 w-5 rounded-full ${classes}`}
    disabled={isRead}
>
    <Icon src={CheckCircle} theme="outline" />
</button>
