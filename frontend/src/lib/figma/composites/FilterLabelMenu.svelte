<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { Search } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { _ } from "svelte-i18n";

    import FilterLabel from "$lib/figma/select-controls/FilterLabel.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import {
        filterByLabel,
        unfilterByLabel,
        labelSearch,
        labelFilterSearchResults,
        selectedLabels,
    } from "$lib/stores/dashboard/labelFilter";
    import type { LabelAssignment } from "$lib/types/stores";
    import type { Label } from "$lib/types/workspace";

    type FilterLabelMenuMode =
        | { kind: "filter"; startUpdate?: (label: Label) => void }
        | {
              kind: "assign";
              labelAssignment: LabelAssignment;
          };

    export let mode: FilterLabelMenuMode;

    $: selected =
        mode.kind === "filter"
            ? selectedLabels
            : mode.labelAssignment.selected;
    $: onCheck =
        mode.kind === "filter" ? filterByLabel : mode.labelAssignment.select;
    $: onUncheck =
        mode.kind === "filter"
            ? unfilterByLabel
            : mode.labelAssignment.deselect;
</script>

<div class="flex flex-col px-4 pb-4">
    <InputField
        bind:value={$labelSearch}
        label={$_("dashboard.side-nav.filter-labels.input.label")}
        style={{ inputType: "text" }}
        name="label-name"
        placeholder={$_("dashboard.side-nav.filter-labels.input.placeholder")}
    >
        <Icon slot="left" src={Search} class="w-4" theme="outline" />
    </InputField>
</div>
<div class="flex flex-col">
    {#if mode.kind == "filter"}
        <FilterLabel
            label={{ kind: "allLabels" }}
            checked={$selected.kind === "allLabels"}
            onCheck={() => filterByLabel({ kind: "allLabels" })}
            onUncheck={() => unfilterByLabel({ kind: "allLabels" })}
        />
    {/if}
    <FilterLabel
        label={{ kind: "noLabel" }}
        checked={$selected.kind === "noLabel"}
        onCheck={() => onCheck({ kind: "noLabel" })}
        onUncheck={() => onUncheck({ kind: "noLabel" })}
    />
    {#each $labelFilterSearchResults as label (label.uuid)}
        <FilterLabel
            label={{ kind: "label", label }}
            checked={$selected.kind === "labels"
                ? $selected.labelUuids.has(label.uuid)
                : false}
            onEdit={mode.kind === "filter"
                ? mode.startUpdate?.bind(null, label)
                : undefined}
            onCheck={() => onCheck({ kind: "label", labelUuid: label.uuid })}
            onUncheck={() =>
                onUncheck({ kind: "label", labelUuid: label.uuid })}
        />
    {/each}
</div>
