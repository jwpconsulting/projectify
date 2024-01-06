<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
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
    import { createLabel, updateLabel } from "$lib/repository/workspace/label";
    import {
        labelExpandOpen,
        toggleLabelDropdownClosedNavOpen,
        currentWorkspace,
    } from "$lib/stores/dashboard";
    import { selectedLabels } from "$lib/stores/dashboard/labelFilter";
    import type { Label } from "$lib/types/workspace";
    import {
        labelColors,
        type LabelColor,
        getIndexFromLabelColor,
        getLabelColorFromIndex,
    } from "$lib/utils/colors";

    // Still exporting this one for better testability in storybook
    // TODO or perhaps we can refactor the form to a new component?
    export let state: FilterLabelMenuState = { kind: "list" };

    let chosenColor: LabelColor | undefined = undefined;
    let labelName: string | undefined = undefined;

    async function createOrUpdate() {
        if (!chosenColor) {
            throw new Error("Expected chosenColor");
        }
        if (!labelName) {
            throw new Error("Expected labelName");
        }
        const color = getIndexFromLabelColor(chosenColor);
        if (state.kind === "update") {
            await updateLabel(
                { ...state.label, name: labelName, color },
                { fetch },
            );
        } else {
            await createLabel(
                currentWorkspace.unwrap(),
                { name: labelName, color },
                { fetch },
            );
        }
        state = { kind: "list" };
    }

    function startCreateLabel() {
        state = { kind: "create" };
        chosenColor = undefined;
        labelName = undefined;
    }

    function cancelCreateOrUpdate() {
        // Reset form
        chosenColor = undefined;
        labelName = undefined;
        // Go back
        state = { kind: "list" };
    }

    function startUpdate(label: Label) {
        state = { kind: "update", label };
        const labelColor = getLabelColorFromIndex(label.color);
        if (!labelColor) {
            console.warn("No color found for", label);
        }
        chosenColor = labelColor ?? labelColors[0];
        labelName = label.name;
    }

    // TODO refactor creation thing into new thing
</script>

<SideNavMenuCategory
    label={$_("dashboard.side-nav.filter-labels.title")}
    icon={Tag}
    on:click={toggleLabelDropdownClosedNavOpen}
    open={$labelExpandOpen}
    filtered={$selectedLabels.kind !== "allLabels"}
/>
{#if $labelExpandOpen}
    <div class="shrink overflow-y-auto">
        {#if state.kind === "list"}
            <FilterLabelMenu mode={{ kind: "filter", startUpdate }} />
            <!-- Some left padding issues here, not aligned with the rest above -->
            <ContextMenuButton
                label={$_("dashboard.side-nav.filter-labels.create-new-label")}
                icon={Plus}
                state="normal"
                color="primary"
                kind={{ kind: "button", action: startCreateLabel }}
            />
        {:else}
            <!-- all this px-4 bizniz is sub-optimal -->
            <form
                class="flex flex-col gap-4 px-4"
                on:submit|preventDefault={createOrUpdate}
            >
                <p>
                    {#if state.kind === "update"}
                        {$_("dashboard.side-nav.filter-labels.state.update", {
                            values: { label: state.label.name },
                        })}
                    {:else}
                        {$_("dashboard.side-nav.filter-labels.state.create")}
                    {/if}
                </p>
                <div class="flex flex-col gap-2">
                    <InputField
                        style={{ inputType: "text" }}
                        placeholder={state.kind === "update"
                            ? $_(
                                  "dashboard.side-nav.filter-labels.update-input.placeholder",
                              )
                            : $_(
                                  "dashboard.side-nav.filter-labels.create-input.placeholder",
                              )}
                        label={state.kind === "update"
                            ? $_(
                                  "dashboard.side-nav.filter-labels.update-input.label",
                              )
                            : $_(
                                  "dashboard.side-nav.filter-labels.create-input.label",
                              )}
                        name="name"
                        bind:value={labelName}
                    />
                    <div class="flex flex-col gap-4">
                        <div class="text-sm font-bold">Select label color</div>
                        <!-- XXX Hacky hacky radio emulation because Svelte wants radio
                inputs to be contained in the same file in order to be grouped
                together -->
                        <fieldset class="flex flex-row flex-wrap gap-3">
                            {#each labelColors as labelColor}
                                <SelectLabelCheckBox
                                    label={{ kind: "createLabel", labelColor }}
                                    checked={chosenColor === labelColor}
                                    onCheck={() => {
                                        chosenColor = labelColor;
                                    }}
                                    onUncheck={() =>
                                        console.debug(
                                            "Should we do something here?",
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
                        label={$_("dashboard.side-nav.filter-labels.cancel")}
                        action={{
                            kind: "button",
                            action: cancelCreateOrUpdate,
                        }}
                    />
                    <Button
                        style={{ kind: "primary" }}
                        color="blue"
                        size="medium"
                        label={$_("dashboard.side-nav.filter-labels.save")}
                        action={{ kind: "submit" }}
                    />
                </div>
            </form>
        {/if}
    </div>
{/if}
