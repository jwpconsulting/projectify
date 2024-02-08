<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2024 JWP Consulting GK

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
    import { _ } from "svelte-i18n";

    import type { FilterLabelMenuState } from "$lib/figma/types";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { createLabel, updateLabel } from "$lib/repository/workspace/label";
    import { currentWorkspace } from "$lib/stores/dashboard";
    import {
        getIndexFromLabelColor,
        type LabelColor,
    } from "$lib/utils/colors";

    import LabelRadio from "./LabelRadio.svelte";

    export let state: FilterLabelMenuState;

    export let chosenColor: LabelColor | undefined = undefined;
    export let labelName: string | undefined = undefined;

    $: canSave = chosenColor !== undefined && labelName !== undefined;

    function cancelCreateOrUpdate() {
        // Reset form
        chosenColor = undefined;
        labelName = undefined;
        // Go back
        state = { kind: "list" };
    }

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
</script>

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
    <div class="flex flex-col gap-4">
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
                ? $_("dashboard.side-nav.filter-labels.update-input.label")
                : $_("dashboard.side-nav.filter-labels.create-input.label")}
            name="label-name"
            bind:value={labelName}
            required
        />
        <LabelRadio bind:chosenColor />
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
            action={{ kind: "submit", disabled: !canSave }}
        />
    </div>
</form>
