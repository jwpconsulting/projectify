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
    import { goto } from "$lib/navigation";
    import {
        createTask,
        type CreateUpdateTaskData,
    } from "$lib/repository/workspace";
    import { createWorkspaceBoardSection } from "$lib/repository/workspace/workspaceBoardSection";
    import { getNewLabelUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { user, workspace, workspaceBoard, workspaceBoardSection } = data;

    let taskTitle: string | undefined = undefined;

    $: workspaceBoardSectionTitle =
        workspaceBoardSection?.title ??
        $_("onboarding.new-task.workspace-board-section-title");

    $: disabled = taskTitle === undefined;
    async function submit() {
        if (!taskTitle) {
            throw new Error("Expected taskTitle");
        }
        const result = await createWorkspaceBoardSection(
            workspaceBoard,
            { title: workspaceBoardSectionTitle },
            { fetch },
        );
        if (!result.ok) {
            throw result.error;
        }
        const workspace_board_section = result.data;
        // Find ourselves
        const assignee = workspace.workspace_users.find(
            (w) => w.user.email === user.email,
        );
        const task: CreateUpdateTaskData = {
            title: taskTitle,
            labels: [],
            workspace_board_section,
            assignee,
        };
        const { uuid } = await createTask(task, { fetch });
        await goto(getNewLabelUrl(uuid));
    }
</script>

<Onboarding
    stepCount={5}
    step={2}
    nextAction={{ kind: "submit", disabled, submit }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.new-task.title")}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        <div class="flex flex-col gap-4">
            <p>
                {#if workspaceBoardSection}
                    {$_("onboarding.new-task.prompt.exists", {
                        values: { workspaceBoardSectionTitle },
                    })}
                {:else}
                    {$_("onboarding.new-task.prompt.location", {
                        values: { workspaceBoardSectionTitle },
                    })}
                {/if}
            </p>
            <p>{$_("onboarding.new-task.prompt.explanation")}</p>
        </div>
    </svelte:fragment>

    <svelte:fragment slot="inputs">
        <InputField
            style={{ inputType: "text" }}
            name="task-title"
            label={$_("onboarding.new-task.input.label")}
            placeholder={$_("onboarding.new-task.input.placeholder")}
            bind:value={taskTitle}
        />
    </svelte:fragment>

    <DashboardPlaceholder
        slot="content"
        state={{
            kind: "new-task",
            workspace,
            workspaceBoard,
            workspaceBoardSectionTitle,
            title: taskTitle ?? $_("onboarding.new-task.default-name"),
        }}
    />
</Onboarding>
