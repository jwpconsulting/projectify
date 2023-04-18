<script lang="ts">
    import { _ } from "svelte-i18n";
    import { createEventDispatcher } from "svelte";
    import type { SelectLabel } from "$lib/figma/types";
    import SelectLabelCheckBox from "$lib/figma/select-controls/SelectLabelCheckBox.svelte";
    import CircleIcon from "$lib/figma/buttons/CircleIcon.svelte";
    import { openDestructiveOverlay } from "$lib/stores/global-ui";
    import { deleteLabel } from "$lib/repository/workspace";

    export let label: SelectLabel;
    export let checked: boolean;
    export let canEdit = true;

    $: editable = label.kind === "label" && canEdit;

    const dispatch = createEventDispatcher();

    function onChecked() {
        checked = true;
    }

    function onUnchecked() {
        checked = false;
    }

    function click() {
        if (checked) {
            dispatch("unchecked");
            checked = false;
        } else {
            dispatch("checked");
            checked = true;
        }
    }

    function onEdit() {
        // TODO
    }

    function onDelete() {
        if (label.kind !== "label") {
            throw new Error("Expected label");
        }
        const l = label.label;
        openDestructiveOverlay(
            { kind: "deleteLabel", label: l },
            {
                kind: "async",
                action: async () => {
                    await deleteLabel(l);
                },
            }
        );
    }
</script>

<button
    class="group flex w-full flex-row items-center justify-between px-5 py-2 hover:bg-base-200"
    on:click={click}
>
    <div class="flex flex-row items-center gap-2">
        <SelectLabelCheckBox
            {label}
            {checked}
            on:checked={onChecked}
            on:unchecked={onUnchecked}
        />
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
            <CircleIcon
                size="small"
                disabled={false}
                icon="edit"
                action={{ kind: "button", action: onEdit }}
            />
            <CircleIcon
                size="small"
                disabled={false}
                icon="delete"
                action={{ kind: "button", action: onDelete }}
            />
        {/if}
    </div>
</button>
