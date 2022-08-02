<script lang="ts">
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
    export let seats: number;
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="group rounded-llg border border-transparent p-0.5 text-xl font-bold focus:border-base-content focus:outline-none"
>
    <div
        class="rounded-lg border border-base-300 px-2 py-1.5 group-hover:bg-secondary group-active:bg-primary-hover group-active:text-base-100"
    >
        {seats}
    </div>
</button>
