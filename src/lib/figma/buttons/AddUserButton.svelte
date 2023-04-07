<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { UserAdd } from "@steeze-ui/heroicons";

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="group h-7 w-7 rounded-full border border-transparent p-0.5 focus:border-base-content focus:outline-none"
>
    <div
        class="rounded-full border border-dashed border-primary p-1 text-primary group-hover:bg-base-200"
    >
        <Icon src={UserAdd} theme="outline" />
    </div>
</button>
