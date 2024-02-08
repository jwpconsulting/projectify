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
    import { _ } from "svelte-i18n";

    import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import { goto } from "$lib/navigation";
    import { updateTask } from "$lib/repository/workspace";
    import { createLabel } from "$lib/repository/workspace/label";
    import type { AuthViewState } from "$lib/types/ui";
    import { getAssignTaskUrl, getNewTaskUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { workspace, workspaceBoard, workspaceBoardSection, task } = data;

    const taskTitle = task.title;
    let labelTitle: string | undefined = undefined;
    let labelTitleValidation: InputFieldValidation | undefined = undefined;

    let state: AuthViewState = { kind: "start" };

    $: disabled = !labelTitle || state.kind === "submitting";

    async function submit() {
        if (!labelTitle) {
            throw new Error("Expected labelTitle");
        }

        state = { kind: "submitting" };
        const result = await createLabel(
            workspace,
            { name: labelTitle, color: 0 },
            { fetch },
        );
        labelTitleValidation = undefined;
        if (!result.ok) {
            if (result.error.name) {
                labelTitleValidation = { ok: false, error: result.error.name };
            }
            state = {
                kind: "error",
                message: $_("onboarding.new-label.error"),
            };
            return;
        }

        const label = result.data;
        await updateTask(
            task,
            { ...task, labels: [label], assignee: task.assignee },
            { fetch },
        );
        // TODO handle if label with this name already exists
        await goto(getAssignTaskUrl(task.uuid));
    }
</script>

<Onboarding
    stepCount={5}
    step={4}
    backAction={{ kind: "a", href: getNewTaskUrl(workspaceBoard.uuid) }}
    nextAction={{ kind: "submit", disabled, submit }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.new-label.title", {
            values: { taskTitle },
        })}</svelte:fragment
    >
    <svelte:fragment slot="prompt"
        ><p>{$_("onboarding.new-label.prompt")}</p></svelte:fragment
    >

    <svelte:fragment slot="inputs">
        <InputField
            style={{ inputType: "text" }}
            name="label-title"
            label={$_("onboarding.new-label.input.label")}
            placeholder={$_("onboarding.new-label.input.placeholder")}
            bind:value={labelTitle}
            validation={labelTitleValidation}
        />
        {#if state.kind === "error"}
            <p>
                {state.message}
            </p>
        {/if}
    </svelte:fragment>

    <DashboardPlaceholder
        slot="content"
        state={{
            kind: "new-label",
            workspace,
            workspaceBoard,
            workspaceBoardSection,
            task,
            title: labelTitle ?? $_("onboarding.new-label.default-name"),
        }}
    />
</Onboarding>
