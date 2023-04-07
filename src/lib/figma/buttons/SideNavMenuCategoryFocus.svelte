<script lang="ts">
    import type { IconSource } from "@steeze-ui/svelte-icon/types";
    import { createEventDispatcher } from "svelte";
    import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";

    export let label: string;
    export let icon: IconSource;
    export let filtered: boolean;
    export let open: boolean;

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    class="group w-full rounded-lg border border-transparent p-0.5 focus:border-base-content focus:outline-none"
    on:click={click}
>
    <SideNavMenuCategory contained={true} {label} {icon} {filtered} {open} />
</button>
