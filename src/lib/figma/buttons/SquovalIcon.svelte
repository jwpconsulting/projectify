<script lang="ts">
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
        Plus,
        Pencil,
        DotsVertical,
        LightBulb,
    } from "@steeze-ui/heroicons";
    import type { SquovalIcon, SquovalState } from "$lib/figma/types";

    export let icon: SquovalIcon;
    $: src = {
        "board": Folder,
        "member": User,
        "label": Tag,
        "bulk": CheckCircle,
        "move": SwitchVertical,
        // TODO rename me to filterMember Justus 2023-02-28
        "filter-member": Users,
        "delete": Trash,
        "ellipsis": DotsHorizontal,
        "plus": Plus,
        "edit": Pencil,
        "dotsVertical": DotsVertical,
        "help": LightBulb,
    }[icon];
    // TODO active state should be renamed to enabled Justus 2023-03-07
    export let state: SquovalState;
    export let active = false;

    export let action: () => void;
</script>

<button
    on:click={action}
    class="focus:base-content relative h-8 w-8 rounded-lg border border-transparent p-1 focus:border-base-content focus:outline-none active:text-display enabled:hover:bg-secondary-hover enabled:active:bg-primary"
    class:text-base-content={state === "active"}
    class:invisible={state === "inactive"}
    class:text-secondary-text={state === "disabled"}
    disabled={state !== "active"}
>
    {#if active}
        <div
            class="-2 border-base absolute top-1 left-5 h-2 w-2 rounded-full border bg-primary"
        />
    {/if}
    <Icon {src} theme="outline" />
</button>
