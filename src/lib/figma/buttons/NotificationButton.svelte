<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Bell } from "@steeze-ui/heroicons";
    const dispatch = createEventDispatcher();
    export let isActive: boolean;
    function click() {
        dispatch("click");
    }
</script>

<button
    class="relative h-11 w-11 rounded-lg border border-transparent p-2.5 text-base-content hover:bg-secondary-hover focus:border-base-content focus:outline-none active:bg-secondary-pressed"
    on:click={click}
>
    {#if isActive}
        <div
            class="absolute left-[21px] top-1/3 h-2 w-2 rounded-full border border-base-100 bg-destructive-hover"
        />
    {/if}
    <Icon src={Bell} theme="outline" />
</button>
