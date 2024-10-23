<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";
    import Fields from "$lib/figma/screens/task/Fields.svelte";
    import TaskLabel from "$lib/figma/screens/task/TaskLabel.svelte";
    import TaskUser from "$lib/figma/screens/task/TaskUser.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type {
        LabelAssignment,
        SubTaskAssignment,
        TeamMemberAssignment,
    } from "$lib/types/stores";

    import UpdateSubTasks from "./UpdateSubTasks.svelte";

    export let action: () => void;

    export let title: string | null;
    export let titleValidation: InputFieldValidation | undefined;
    export let description: string | null;
    export let descriptionValidation: string | undefined;
    export let dueDate: string | null;
    export let dueDateValidation: InputFieldValidation | undefined;

    export let teamMemberAssignment: TeamMemberAssignment;
    export let teamMemberAssignmentValidation: string | undefined;
    export let labelAssignment: LabelAssignment;
    export let labelAssignmentValidation: string | undefined;
    export let subTaskAssignment: SubTaskAssignment;
    export let subTaskAssignmentValidation: string | undefined;

    async function showUpdateTeamMember(anchor: HTMLElement) {
        await openContextMenu(
            {
                kind: "updateTeamMember",
                teamMemberAssignment,
            },
            anchor,
        );
    }
    async function showUpdateLabel(anchor: HTMLElement) {
        await openContextMenu(
            {
                kind: "updateLabel",
                labelAssignment,
            },
            anchor,
        );
    }
</script>

<form on:submit|preventDefault={action} id="task-form">
    <!-- TODO remove this hidden submit input -->
    <input type="submit" class="hidden" />
    <Fields>
        <InputField
            slot="title"
            name="title"
            style={{ inputType: "text" }}
            bind:value={title}
            label={undefined}
            placeholder={$_("task-screen.form.title.placeholder")}
            required
            validation={titleValidation}
        />
        <svelte:fragment slot="assignee">
            <TaskUser
                onInteract={showUpdateTeamMember}
                teamMember={$teamMemberAssignment}
            />
            {#if teamMemberAssignmentValidation}<p>
                    {teamMemberAssignmentValidation}
                </p>{/if}
        </svelte:fragment>
        <svelte:fragment slot="labels">
            <TaskLabel
                onInteract={showUpdateLabel}
                labels={$labelAssignment}
            />
            {#if labelAssignmentValidation}<p>
                    {labelAssignmentValidation}
                </p>{/if}
        </svelte:fragment>
        <svelte:fragment slot="due-date">
            <div class="flex flex-row items-center gap-4">
                <InputField
                    bind:value={dueDate}
                    label={undefined}
                    placeholder={$_("task-screen.form.due-date.placeholder")}
                    name="due-date"
                    style={{ inputType: "date" }}
                    validation={dueDateValidation}
                />
            </div>
        </svelte:fragment>
        <svelte:fragment slot="description">
            <textarea
                class="w-full rounded-lg border border-border p-2"
                rows="5"
                name="description"
                id="description"
                bind:value={description}
                placeholder={$_("task-screen.form.description.placeholder")}
            />
            {#if descriptionValidation}<p>{descriptionValidation}</p>{/if}
        </svelte:fragment>
    </Fields>
    {#if subTaskAssignmentValidation}<p>{subTaskAssignmentValidation}</p>{/if}
    <UpdateSubTasks {subTaskAssignment} />
</form>
