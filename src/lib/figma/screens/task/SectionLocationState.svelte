<script lang="ts">
    import { createEventDispatcher } from "svelte";

    export let label: string;

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="rounded-lg border border-transparent bg-task-hover p-2 text-xxs font-bold hover:bg-task-pressed focus:border-border-focus focus:bg-background focus:outline-none active:bg-secondary-hover"
>
    {label}
</button>
