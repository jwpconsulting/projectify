<script lang="ts">
    import { _ } from "svelte-i18n";
    import FilterLabelMenu from "$lib/figma/composites/FilterLabelMenu.svelte";
    import type { SelectLabel, FilterLabelMenuState } from "$lib/figma/types";
    import type { LabelSearchModule } from "$lib/types/stores";
    import InputField from "$lib/figma/input-fields/InputField.svelte";
    import Button from "$lib/figma/buttons/Button.svelte";
    import SelectLabelCheckBox from "$lib/figma/select-controls/SelectLabelCheckBox.svelte";
    import type { Label } from "$lib/types/workspace";
    import { labelColors } from "$lib/utils/colors";

    export let labelSearchModule: LabelSearchModule;

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

    const makeIsLabelSelected = (color: null | number) =>
        Object.fromEntries(labelColors.map((_name, ix) => [ix, ix === color]));
    let isLabelSelected: { [key: number]: boolean } =
        makeIsLabelSelected(null);

    $: {
        if (chosenColor) {
            isLabelSelected = makeIsLabelSelected(chosenColor.color);
        }
    }
</script>

{#if state === "list"}
    <FilterLabelMenu {labelSearchModule} />
{:else}
    <form class="flex flex-col gap-6">
        <div class="flex flex-col">
            <div class="px-4 pt-2 pb-4">
                <InputField
                    style={{ kind: "field", inputType: "text" }}
                    placeholder={$_("filter-label-menu.label-name")}
                    label={$_("filter-label-menu.label-name")}
                    name="name"
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
                disabled={false}
            />
            <Button
                style={{ kind: "primary" }}
                color="blue"
                size="medium"
                label={$_("filter-label-menu.save")}
                disabled={false}
            />
        </div>
    </form>
{/if}
