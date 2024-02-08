<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023-2024 JWP Consulting GK

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
    import type { FilterLabelMenuState } from "$lib/figma/types";
    import {
        labelExpandOpen,
        toggleLabelDropdownClosedNavOpen,
    } from "$lib/stores/dashboard";
    import { selectedLabels } from "$lib/stores/dashboard/labelFilter";
    import type { Label } from "$lib/types/workspace";
    import {
        labelColors,
        type LabelColor,
        getLabelColorFromIndex,
    } from "$lib/utils/colors";

    import CreateOrUpdateLabel from "./filter-labels/CreateOrUpdateLabel.svelte";

    // Still exporting this one for better testability in storybook
    // TODO or perhaps we can refactor the form to a new component?
    export let state: FilterLabelMenuState = { kind: "list" };

    let chosenColor: LabelColor | undefined = undefined;
    let labelName: string | undefined = undefined;

    function startCreateLabel() {
        state = { kind: "create" };
        chosenColor = undefined;
        labelName = undefined;
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

    function onCreateOrUpdateFinish() {
        state = { kind: "list" };
    }
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
            <CreateOrUpdateLabel
                onFinished={onCreateOrUpdateFinish}
                {state}
                bind:chosenColor
                bind:labelName
            />
        {/if}
    </div>
{/if}
