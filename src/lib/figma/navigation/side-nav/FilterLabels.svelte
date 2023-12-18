<script lang="ts">
    import { Tag, Plus } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import SideNavMenuCategory from "$lib/figma/buttons/SideNavMenuCategory.svelte";
    import FilterLabelMenu from "$lib/figma/composites/FilterLabelMenu.svelte";
    import SelectLabelCheckBox from "$lib/figma/select-controls/SelectLabelCheckBox.svelte";
    import type { FilterLabelMenuState } from "$lib/figma/types";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { createLabel } from "$lib/repository/workspace/label";
    import {
        labelExpandOpen,
        toggleLabelDropdownClosedNavOpen,
        currentWorkspace,
    } from "$lib/stores/dashboard";
    import { selectedLabels } from "$lib/stores/dashboard/labelFilter";
    import {
        labelColors,
        type LabelColor,
        getIndexFromLabelColor,
    } from "$lib/utils/colors";

    // Still exporting this one for better testability in storybook
    // TODO or perhaps we can refactor the form to a new component?
    export let state: FilterLabelMenuState = { kind: "list" };

    let chosenColor: LabelColor | undefined = undefined;
    let labelName: string | undefined = undefined;

    async function save() {
        if (!chosenColor) {
            throw new Error("Expected chosenColor");
        }
        if (!labelName) {
            throw new Error("Expected labelName");
        }
        await createLabel(
            currentWorkspace.unwrap(),
            { name: labelName, color: getIndexFromLabelColor(chosenColor) },
            { fetch }
        );
        state = { kind: "list" };
    }

    function startCreateLabel() {
        state = { kind: "create" };
    }

    function cancelCreate() {
        // Reset form
        chosenColor = undefined;
        labelName = undefined;
        // Go back
        state = { kind: "list" };
    }

    // TODO refactor creation thing into new thing
</script>

<SideNavMenuCategory
    label={$_("dashboard.labels")}
    icon={Tag}
    on:click={toggleLabelDropdownClosedNavOpen}
    open={$labelExpandOpen}
    filtered={$selectedLabels.kind !== "allLabels"}
/>
{#if $labelExpandOpen}
    <div class="shrink overflow-y-auto">
        {#if state.kind === "list"}
            <FilterLabelMenu mode={{ kind: "filter" }} />
            <!-- Some left padding issues here, not aligned with the rest above -->
            <ContextMenuButton
                label={$_("filter-label-menu.create-new-label")}
                icon={Plus}
                state="normal"
                color="primary"
                kind={{ kind: "button", action: startCreateLabel }}
            />
        {:else if state.kind === "create"}
            <form class="flex flex-col gap-4" on:submit|preventDefault={save}>
                <div class="flex flex-col gap-2">
                    <InputField
                        style={{ inputType: "text" }}
                        placeholder={$_("filter-label-menu.label-name")}
                        label={$_("filter-label-menu.label-name")}
                        name="name"
                        bind:value={labelName}
                    />
                    <div class="flex flex-col gap-4">
                        <div class="text-sm font-bold">Select label color</div>
                        <!-- XXX Hacky hacky radio emulation because Svelte wants radio
                inputs to be contained in the same file in order to be grouped
                together -->
                        <fieldset class="flex flex-row flex-wrap gap-7">
                            {#each labelColors as labelColor}
                                <SelectLabelCheckBox
                                    label={{ kind: "createLabel", labelColor }}
                                    checked={chosenColor === labelColor}
                                    onCheck={() => {
                                        chosenColor = labelColor;
                                    }}
                                    onUncheck={() =>
                                        console.debug(
                                            "Should we do something here?"
                                        )}
                                    name="label-color-{labelColor}"
                                />
                            {/each}
                        </fieldset>
                    </div>
                </div>
                <div class="flex flex-row gap-4">
                    <Button
                        style={{ kind: "secondary" }}
                        color="blue"
                        size="medium"
                        label={$_("filter-label-menu.cancel")}
                        action={{ kind: "button", action: cancelCreate }}
                    />
                    <Button
                        style={{ kind: "primary" }}
                        color="blue"
                        size="medium"
                        label={$_("filter-label-menu.save")}
                        action={{ kind: "button", action: save }}
                    />
                </div>
            </form>
        {:else if state.kind === "update"}
            updating label
        {/if}
    </div>
{/if}
