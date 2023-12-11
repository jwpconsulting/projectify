<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { _ } from "svelte-i18n";

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="inline-block rounded-2.5xl bg-destructive-secondary-hover px-2 py-1 text-sm font-bold"
>
    {$_("task-screen.due-soon")}
</button>
