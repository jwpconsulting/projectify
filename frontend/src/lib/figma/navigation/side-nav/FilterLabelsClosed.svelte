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
    // Refactor these
    // TODO Justus 2023-05-03
    import SelectLabelCheckBox from "$lib/figma/select-controls/SelectLabelCheckBox.svelte";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import {
        filterByLabel,
        selectedLabels,
        labelFilterSearchResults,
        unfilterByLabel,
    } from "$lib/stores/dashboard/labelFilter";
    import {
        labelExpandOpen,
        toggleLabelDropdownClosedNavOpen,
    } from "$lib/stores/dashboard/ui";
</script>

<div class="flex flex-col items-center gap-6">
    <SquovalIcon
        state="active"
        icon="label"
        action={{ kind: "button", action: toggleLabelDropdownClosedNavOpen }}
        active={$selectedLabels.kind !== "allLabels"}
    />
    {#if $labelExpandOpen}
        <div class="flex flex-col items-center gap-2">
            <SelectLabelCheckBox
                label={{ kind: "allLabels" }}
                checked={$selectedLabels.kind === "allLabels"}
                onCheck={() => filterByLabel({ kind: "allLabels" })}
                onUncheck={() => unfilterByLabel({ kind: "allLabels" })}
            />
            <SelectLabelCheckBox
                label={{ kind: "noLabel" }}
                checked={$selectedLabels.kind === "noLabel"}
                onCheck={() => filterByLabel({ kind: "noLabel" })}
                onUncheck={() => unfilterByLabel({ kind: "noLabel" })}
            />
            {#each $labelFilterSearchResults as label}
                <SelectLabelCheckBox
                    label={{ kind: "label", label: label }}
                    checked={$selectedLabels.kind === "labels"
                        ? $selectedLabels.labelUuids.has(label.uuid)
                        : false}
                    onCheck={() =>
                        filterByLabel({
                            kind: "label",
                            labelUuid: label.uuid,
                        })}
                    onUncheck={() =>
                        unfilterByLabel({
                            kind: "label",
                            labelUuid: label.uuid,
                        })}
                />
            {/each}
        </div>
    {/if}
</div>
