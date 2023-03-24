<script lang="ts">
    import { _ } from "svelte-i18n";
    import LabelPill from "$lib/components/dashboard/LabelPill.svelte";
    import type { Label } from "$lib/types/workspace";
    import { currentWorkspace, loading } from "$lib/stores/dashboard";
    import {
        createLabel,
        deleteLabel,
        updateLabel,
    } from "$lib/repository/workspace";

    let labels: Label[] = [];

    $: {
        if ($currentWorkspace && $currentWorkspace.labels) {
            labels = $currentWorkspace.labels;
            $loading = false;
        } else {
            $loading = true;
        }
    }

    async function onDeleteLabel(label: Label) {
        // TODO let modalRes = await getModal("deleteLabel").open();
        // TODO if (!modalRes) {
        // TODO     return;
        // TODO }
        // TODO await deleteLabel(label);
    }

    async function onEditLabel(label: Label) {
        // TODO let modalRes = await getModal("editLabel").open({ ...label });
        // TODO if (!modalRes) {
        // TODO     return;
        // TODO }
        // TODO await updateLabel(
        // TODO     label,
        // TODO     modalRes.outputs.name,
        // TODO     modalRes.outputs.color
        // TODO );
    }

    async function onNewLabel() {
        // TODO let modalRes = await getModal("newLabel").open();
        // TODO if (!modalRes) {
        // TODO     return;
        // TODO }
        // TODO if (!$currentWorkspace) {
        // TODO     return;
        // TODO }
        // TODO await createLabel(
        // TODO     $currentWorkspace,
        // TODO     modalRes.outputs.name,
        // TODO     modalRes.outputs.color
        // TODO );
    }
</script>

<div class=" divide-y divide-base-300">
    {#each labels as label}
        <div class="flex space-x-4 py-4">
            <div class="flex grow">
                <LabelPill {label} />
            </div>
            <div class="flex items-center space-x-2">
                <button
                    on:click={() => onEditLabel(label)}
                    class="btn btn-primary btn-ghost btn-sm btn-sm rounded-full text-primary"
                >
                    {$_("Edit")}
                </button>
                <button
                    on:click={() => onDeleteLabel(label)}
                    class="btn btn-outline btn-accent btn-sm rounded-full"
                >
                    {$_("Delete")}
                </button>
            </div>
        </div>
    {/each}
    <div class="py-2">
        <a
            href="/"
            on:click|preventDefault={onNewLabel}
            class="ch flex space-x-4 p-2"
        >
            <div
                class="flex grow flex-col justify-center font-bold text-primary"
            >
                + {$_("new-label")}
            </div>
        </a>
    </div>
</div>
