<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Camera } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    class="group h-14 w-14 rounded-full border border-transparent p-0.5 focus:border-primary-hover"
    on:click={click}
>
    <div
        class="rounded-full border border-primary p-3 text-primary group-hover:bg-secondary"
    >
        <Icon src={Camera} theme="outline" />
    </div>
</button>
