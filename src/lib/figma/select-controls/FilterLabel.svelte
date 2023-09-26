<script lang="ts">
    import { _ } from "svelte-i18n";

    import SelectLabelCheckBox from "$lib/figma/select-controls/SelectLabelCheckBox.svelte";
    import type { SelectLabel } from "$lib/figma/types";
    import CircleIcon from "$lib/funabashi/buttons/CircleIcon.svelte";
    import { deleteLabel } from "$lib/repository/workspace";
    import { openDestructiveOverlay } from "$lib/stores/globalUi";

    export let label: SelectLabel;
    export let checked: boolean;
    export let canEdit = true;

    export let onCheck: () => void;
    export let onUncheck: () => void;

    $: editable = label.kind === "label" && canEdit;

    function click() {
        // TODO use callback props
        //  Justus 2023-09-19
        if (checked) {
            onCheck();
            checked = false;
        } else {
            onUncheck();
            checked = true;
        }
    }

    function onEdit() {
        // TODO
    }

    async function onDelete() {
        if (label.kind !== "label") {
            throw new Error("Expected label");
        }
        const l = label.label;
        await openDestructiveOverlay({ kind: "deleteLabel", label: l });
        await deleteLabel(l);
    }
</script>

<button
    class="group flex w-full flex-row items-center justify-between px-5 py-2 hover:bg-base-200"
    on:click={click}
>
    <div class="flex min-w-0 flex-row items-center gap-2">
        <SelectLabelCheckBox {label} bind:checked {onCheck} {onUncheck} />
        <div class="text-regular truncate text-xs">
            {#if label.kind === "allLabels"}
                {$_("filter-label.all")}
            {:else if label.kind === "noLabel"}
                {$_("filter-label.none")}
            {:else if label.kind === "label"}
                {label.label.name}
            {/if}
        </div>
    </div>
    <div class="flex flex-row items-center gap-2">
        {#if editable}
            <CircleIcon
                size="small"
                icon="edit"
                action={{ kind: "button", action: onEdit }}
            />
            <CircleIcon
                size="small"
                icon="delete"
                action={{ kind: "button", action: onDelete }}
            />
        {/if}
    </div>
</button>
