<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

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
        ariaLabel={$labelExpandOpen
            ? $_("dashboard.side-nav.filter-labels.close-collapsible")
            : $_("dashboard.side-nav.filter-labels.open-collapsible")}
    />
    {#if $labelExpandOpen}
        <div class="flex flex-col items-center gap-2">
            <label class="sr-only" for="select-all-labels">
                {$_("filter-label.all")}
            </label>
            <SelectLabelCheckBox
                label={{ kind: "allLabels" }}
                checked={$selectedLabels.kind === "allLabels"}
                onCheck={() => filterByLabel({ kind: "allLabels" })}
                onUncheck={() => unfilterByLabel({ kind: "allLabels" })}
                id="select-all-labels"
            />
            <label class="sr-only" for="select-no-label">
                {$_("filter-label.none")}
            </label>
            <SelectLabelCheckBox
                label={{ kind: "noLabel" }}
                checked={$selectedLabels.kind === "noLabel"}
                onCheck={() => filterByLabel({ kind: "noLabel" })}
                onUncheck={() => unfilterByLabel({ kind: "noLabel" })}
                id="select-no-label"
            />
            {#each $labelFilterSearchResults as label}
                <label class="sr-only" for="select-{label.uuid}">
                    {label.name}
                </label>
                <SelectLabelCheckBox
                    label={{ kind: "label", label: label }}
                    id="select-{label.uuid}"
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
