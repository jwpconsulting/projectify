<script lang="ts">
    import { createEventDispatcher } from "svelte";
    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="flex-start flex max-w-fit flex-row p-2.5 text-sm uppercase text-secondary-text hover:text-base-content active:text-base-content"
>
    <slot />
</button>
