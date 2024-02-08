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
    import { onMount } from "svelte";
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import { createLabel, updateLabel } from "$lib/repository/workspace/label";
    import { currentWorkspace } from "$lib/stores/dashboard";
    import type { AuthViewState } from "$lib/types/ui";
    import type { Label } from "$lib/types/workspace";
    import {
        getIndexFromLabelColor,
        getLabelColorFromIndex,
        labelColors,
        type LabelColor,
    } from "$lib/utils/colors";

    import LabelRadio from "./LabelRadio.svelte";

    export let state: { kind: "create" } | { kind: "update"; label: Label };
    export let onFinished: () => void;

    let chosenColor: LabelColor | undefined = undefined;
    let chosenColorValidation: InputFieldValidation | undefined = undefined;
    let labelName: string | undefined = undefined;
    let labelNameValidation: InputFieldValidation | undefined = undefined;

    let editState: AuthViewState = { kind: "start" };

    onMount(() => {
        if (state.kind === "create") {
            return;
        }
        const { label } = state;
        const labelColor = getLabelColorFromIndex(label.color);
        if (!labelColor) {
            console.warn("No color found for", label);
        }
        chosenColor = labelColor ?? labelColors[0];
        labelName = label.name;
    });

    // We can only save if
    // 1) both fields are non-empty,
    // 2) we are not submitting already
    $: canSave =
        chosenColor !== undefined &&
        labelName !== undefined &&
        editState.kind != "submitting";

    async function create() {
        if (!chosenColor) {
            throw new Error("Expected chosenColor");
        }
        if (!labelName) {
            throw new Error("Expected labelName");
        }
        if (state.kind !== "create") {
            throw new Error("Expected create state");
        }

        editState = { kind: "submitting" };
        labelNameValidation = undefined;
        chosenColorValidation = undefined;

        const color = getIndexFromLabelColor(chosenColor);
        const response = await createLabel(
            currentWorkspace.unwrap(),
            { name: labelName, color },
            { fetch },
        );
        if (response.ok) {
            editState = { kind: "start" };
            onFinished();
            return;
        }
        if (response.error.name !== undefined) {
            labelNameValidation = { ok: false, error: response.error.name };
        }
        if (response.error.color !== undefined) {
            chosenColorValidation = { ok: false, error: response.error.color };
        }
        editState = {
            kind: "error",
            message: $_("dashboard.side-nav.filter-labels.errors.create"),
        };
    }

    async function update() {
        if (!chosenColor) {
            throw new Error("Expected chosenColor");
        }
        if (!labelName) {
            throw new Error("Expected labelName");
        }
        if (state.kind !== "update") {
            throw new Error("Expected update state");
        }

        editState = { kind: "submitting" };
        labelNameValidation = undefined;
        chosenColorValidation = undefined;

        const color = getIndexFromLabelColor(chosenColor);
        const response = await updateLabel(
            { ...state.label, name: labelName, color },
            { fetch },
        );
        if (response.ok) {
            editState = { kind: "start" };
            onFinished();
            return;
        }
        if (response.error.name !== undefined) {
            labelNameValidation = { ok: false, error: response.error.name };
        }
        if (response.error.color !== undefined) {
            chosenColorValidation = { ok: false, error: response.error.color };
        }
        editState = {
            kind: "error",
            message: $_("dashboard.side-nav.filter-labels.errors.update"),
        };
    }
</script>

<!-- all this px-4 bizniz is sub-optimal -->
<form
    class="flex flex-col gap-4 px-4"
    on:submit|preventDefault={state.kind === "create" ? create : update}
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
            validation={labelNameValidation}
            required
        />
        <LabelRadio bind:chosenColor />
        {#if chosenColorValidation && !chosenColorValidation.ok}
            <p>{chosenColorValidation.error}</p>
        {/if}
    </div>
    {#if editState.kind === "error"}
        <p>
            {editState.message}
        </p>
    {/if}
    <div class="flex flex-row gap-4">
        <Button
            style={{ kind: "secondary" }}
            color="blue"
            size="medium"
            label={$_("dashboard.side-nav.filter-labels.cancel")}
            action={{
                kind: "button",
                action: onFinished,
                disabled: editState.kind === "submitting",
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
