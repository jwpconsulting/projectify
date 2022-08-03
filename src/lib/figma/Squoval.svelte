<script lang="ts">
    import { createEventDispatcher } from "svelte";

    import { Icon } from "@steeze-ui/svelte-icon";
    import {
        Folder,
        User,
        Tag,
        CheckCircle,
        SwitchVertical,
        Users,
        Trash,
        DotsHorizontal,
    } from "@steeze-ui/heroicons";
    import type { SquovalIcon, SquovalState } from "$lib/figma/types";

    export let icon: SquovalIcon;
    $: src = {
        "board": Folder,
        "member": User,
        "label": Tag,
        "bulk": CheckCircle,
        "move": SwitchVertical,
        "filter-member": Users,
        "delete": Trash,
        "ellipsis": DotsHorizontal,
    }[icon];
    export let state: SquovalState;

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    on:click={click}
    class="focus:base-content h-8 w-8 rounded-lg border border-transparent p-1 focus:border-base-content focus:outline-none active:text-display enabled:hover:bg-secondary-hover enabled:active:bg-primary"
    class:text-base-content={state === "active"}
    class:invisible={state === "inactive"}
    class:text-secondary-text={state === "disabled"}
    disabled={state !== "active"}
>
    <Icon {src} theme="outline" />
</button>
