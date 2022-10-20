<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { DotsHorizontal } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";

    const dispatch = createEventDispatcher();

    function click() {
        dispatch("click");
    }
</script>

<button
    class="group h-7 w-7 rounded-full border border-transparent p-px focus:border-base-content focus:outline-none"
    on:click={click}
>
    <div
        class="rounded-full border border-primary p-0.5 text-primary group-hover:bg-base-200 group-active:bg-primary group-active:text-base-100"
    >
        <Icon src={DotsHorizontal} theme="outline" />
    </div>
</button>
