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
    // This is a partial used inside TaskCard
    // The label picker is TODO
    import { _ } from "svelte-i18n";

    import LabelPill from "$lib/components/dashboard/LabelPill.svelte";
    import { updateTask } from "$lib/repository/workspace";
    import { createLabelAssignment } from "$lib/stores/dashboard/labelAssignment";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { LabelAssignment } from "$lib/types/stores";
    import type { ContextMenuType } from "$lib/types/ui";
    import type {
        Label,
        TaskWithWorkspaceBoardSection,
    } from "$lib/types/workspace";

    export let task: TaskWithWorkspaceBoardSection;

    let labelPickerOpen = false;

    let labelAssignment: LabelAssignment;
    $: {
        if (!labelPickerOpen) {
            labelAssignment = createLabelAssignment(task);
        }
    }

    $: labels = $labelAssignment ?? task.labels;

    async function openLabelPicker(event: MouseEvent) {
        labelPickerOpen = true;
        if (!$labelAssignment) {
            throw new Error("Expected $labelAssignment");
        }
        const anchor = event.target;
        if (!(anchor instanceof HTMLElement)) {
            throw new Error("Expected HTMLElement");
        }
        const contextMenuType: ContextMenuType = {
            kind: "updateLabel",
            labelAssignment,
        };
        // By locking labelAssignment with labelPickerOpen, we prevent the
        // following race condition from happening:
        // 1. update task 1's labels using the label picker
        // 2. while the update request is stil happening, open task 2's label
        // picker
        // 3. wait for task 1's request to finish - the workspace board will
        // re-render
        // 4. click on any label, it the labels shown in the task card
        // will not refresh
        // Reason: labelAssignment is recreated (as a reactive dependency of
        // task). When we arrive in labels = $labelAssignment, we are
        // retrieving the newly created labelAssignment store's values.
        // Mitigation ideas:
        // 1. Lock the dashboard until the label is updated
        // 2. Ensure we don't recreate labelAssignment (what is a component
        // lifecycle in Svelte anyway?! Research)
        // TODO: Think on it
        try {
            await openContextMenu(contextMenuType, anchor);

            const labels: Label[] = $labelAssignment;
            // TODO skip update when no changes detected
            await updateTask(
                task,
                { ...task, labels },
                {
                    fetch,
                },
            );
        } finally {
            labelPickerOpen = false;
        }
        // TODO There is a brief flash after updateTask finishes, the task is
        // reloaded and labelAssignment is recreated
    }
</script>

{#if labels.length}
    <div class="flex flex-row">
        {#each labels as label}
            <button on:click|preventDefault={openLabelPicker}>
                <LabelPill {label} />
            </button>
        {/each}
    </div>
{:else}
    <div class="p-0.5">
        <button
            class="flex flex-row items-center rounded-xl border border-dashed border-primary px-4 py-1 text-sm font-bold text-primary"
            on:click|preventDefault={openLabelPicker}
        >
            {$_("dashboard.task-card.add-label")}</button
        >
    </div>
{/if}
