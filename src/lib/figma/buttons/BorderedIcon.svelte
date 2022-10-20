<script lang="ts">
    import { createEventDispatcher } from "svelte";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Briefcase, Adjustments } from "@steeze-ui/heroicons";
    import type { BorderedIconType } from "$lib/figma/types";

    export let type: BorderedIconType;

    $: src = {
        workspace: Briefcase,
        filter: Adjustments,
    }[type];

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="group h-9 w-9 rounded-llg border border-transparent p-0.5 focus:border-base-content focus:outline-none"
>
    <div
        class="rounded-lg border border-border p-1 group-hover:bg-secondary-hover group-active:bg-primary group-active:text-base-100"
    >
        <Icon {src} theme="outline" />
    </div>
</button>
