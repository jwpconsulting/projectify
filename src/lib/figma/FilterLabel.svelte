<script lang="ts">
    import { _ } from "svelte-i18n";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Pencil, Trash } from "@steeze-ui/heroicons";
    import type { SelectLabel } from "$lib/figma/types";
    import { createEventDispatcher } from "svelte";
    import SelectLabelFocus from "$lib/figma/SelectLabelFocus.svelte";

    export let label: SelectLabel;
    export let selected: boolean;

    $: editable = label.kind === "label";

    const dispatch = createEventDispatcher();
    function click() {
        dispatch("click");
    }
</script>

<button
    class="group flex w-full flex-row items-center justify-between px-5 py-2 hover:bg-base-200"
    on:click={click}
>
    <div class="flex flex-row items-center gap-2">
        <SelectLabelFocus {label} checked={selected} contained={true} />
        <div class="text-regular text-xs capitalize">
            {#if label.kind === "allLabels"}
                {$_("filter-label.all")}
            {:else if label.kind === "noLabel"}
                {$_("filter-label.none")}
            {:else}
                {label.label.name}
            {/if}
        </div>
    </div>
    <div class="flex flex-row items-center gap-2">
        {#if editable}
            <button class="p-1">
                <Icon src={Pencil} theme="outline" class="h-4 w-4" />
            </button>
            <button class="p-1">
                <Icon src={Trash} theme="outline" class="h-4 w-4" />
            </button>
        {/if}
    </div>
</button>
