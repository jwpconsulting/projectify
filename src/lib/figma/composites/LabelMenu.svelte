<script lang="ts">
    import { _ } from "svelte-i18n";

    import FilterLabelMenu from "$lib/figma/composites/FilterLabelMenu.svelte";
    import SelectLabelCheckBox from "$lib/figma/select-controls/SelectLabelCheckBox.svelte";
    import type { SelectLabel, FilterLabelMenuState } from "$lib/figma/types";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { createLabel } from "$lib/repository/workspace";
    import { currentWorkspace } from "$lib/stores/dashboard";
    import type { Label } from "$lib/types/workspace";
    import { labelColors } from "$lib/utils/colors";

    // Still exporting this one for better testability in storybook
    // TODO or perhaps we can refactor the form to a new component?
    export let state: FilterLabelMenuState = "list";

    // TODO cancel callback
    // TODO save callback

    const labelColorChoices: SelectLabel[] = labelColors.map((name, i) => {
        return {
            kind: "label",
            label: {
                uuid: "i-dont-exist",
                color: i,
                name,
            },
        };
    });

    let chosenColor: Label | null = null;
    let labelName: string | undefined = undefined;

    const makeIsLabelSelected = (color: null | number) =>
        Object.fromEntries(labelColors.map((_name, ix) => [ix, ix === color]));
    let isLabelSelected: Record<number, boolean> = makeIsLabelSelected(null);

    $: {
        if (chosenColor) {
            isLabelSelected = makeIsLabelSelected(chosenColor.color);
        }
    }

    async function save() {
        if (!$currentWorkspace) {
            throw new Error("Expected createLabel");
        }
        if (!chosenColor) {
            throw new Error("Expected chosenColor");
        }
        if (!labelName) {
            throw new Error("Expected labelName");
        }
        await createLabel($currentWorkspace, labelName, chosenColor.color);
        state = "list";
    }

    function startCreateLabel() {
        state = "create";
    }

    function cancelCreate() {
        // Reset form
        chosenColor = null;
        labelName = undefined;
        // Go back
        state = "list";
    }
</script>

{#if state === "list"}
    <FilterLabelMenu {startCreateLabel} mode={{ kind: "filter" }} />
{:else if state === "create"}
    <form class="flex flex-col gap-6" on:submit|preventDefault={save}>
        <div class="flex flex-col">
            <div class="px-4 pb-4 pt-2">
                <InputField
                    style={{ kind: "field", inputType: "text" }}
                    placeholder={$_("filter-label-menu.label-name")}
                    label={$_("filter-label-menu.label-name")}
                    name="name"
                    bind:value={labelName}
                />
            </div>
            <div class="flex flex-col gap-4 px-7">
                <div class="text-xs font-bold">Select label color</div>
                <!-- XXX Hacky hacky radio emulation because Svelte wants radio
                inputs to be contained in the same file in order to be grouped
                together -->
                <fieldset class="flex flex-row flex-wrap gap-7">
                    {#each labelColorChoices as label, ix}
                        <SelectLabelCheckBox
                            {label}
                            checked={isLabelSelected[ix]}
                            on:checked={() => {
                                if (label.kind != "label") {
                                    throw new Error(
                                        "Going down the sad code path"
                                    );
                                }
                                chosenColor = label.label;
                            }}
                            name="label-color"
                        />
                    {/each}
                </fieldset>
            </div>
        </div>
        <div class="flex flex-row gap-4 px-2">
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
{/if}
