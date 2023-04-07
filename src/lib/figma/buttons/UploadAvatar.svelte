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
    class="focus:border-focus group h-14 w-14 rounded-full border border-transparent p-0.5"
    on:click={click}
>
    <div
        class="rounded-full border border-primary bg-foreground p-3 text-primary group-hover:bg-secondary-hover group-active:bg-disabled"
    >
        <Icon src={Camera} theme="outline" />
    </div>
</button>
