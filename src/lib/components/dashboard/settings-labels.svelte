<script lang="ts">
    import { client } from "$lib/graphql/client";

    import {
        Mutation_AddLabelMutation,
        Mutation_DeleteLabelMutation,
        Mutation_UpdateLabelMutation,
        Query_WorkspaceLabels,
    } from "$lib/graphql/operations";
    import { getSubscriptionForCollection } from "$lib/stores/dashboardSubscription";
    import debounce from "lodash/debounce.js";
    import { query } from "svelte-apollo";
    import { _ } from "svelte-i18n";
    import ConfirmModalContent from "../confirmModalContent.svelte";
    import DialogModal, { getModal } from "../dialogModal.svelte";
    import Loading from "../loading.svelte";
    import LabelPill from "./labelPill.svelte";

    export let workspaceUUID = null;

    let res = null;
    let workspaceWSStore;
    let workspace = null;
    let labels = [];

    const refetch = debounce(() => {
        res.refetch();
    }, 100);

    $: {
        if (workspaceUUID) {
            res = query(Query_WorkspaceLabels, {
                variables: { uuid: workspaceUUID },
                fetchPolicy: "network-only",
            });

            workspaceWSStore = getSubscriptionForCollection(
                "workspace",
                workspaceUUID
            );
        }
    }

    $: {
        if ($workspaceWSStore) {
            refetch();
        }
    }

    $: {
        if (res && $res.data) {
            workspace = $res.data["workspace"];
            if (workspace["labels"]) {
                labels = workspace["labels"];
            }
        }
    }

    async function onDeleteLabel(label) {
        let modalRes = await getModal("deleteLabel").open();

        if (!modalRes) {
            return;
        }

        try {
            await client.mutate({
                mutation: Mutation_DeleteLabelMutation,
                variables: {
                    input: {
                        uuid: label.uuid,
                    },
                },
            });

            refetch();
        } catch (error) {
            console.error(error);
        }
    }

    async function onEditLabel(label) {
        let modalRes = await getModal("editLabel").open({ ...label });

        if (!modalRes) {
            return;
        }

        try {
            await client.mutate({
                mutation: Mutation_UpdateLabelMutation,
                variables: {
                    input: {
                        uuid: label.uuid,
                        name: modalRes.outputs.name,
                        color: modalRes.outputs.color,
                    },
                },
            });

            refetch();
        } catch (error) {
            console.error(error);
        }
    }

    async function onNewLabel() {
        let modalRes = await getModal("newLabel").open();

        if (!modalRes) {
            return;
        }

        try {
            await client.mutate({
                mutation: Mutation_AddLabelMutation,
                variables: {
                    input: {
                        workspaceUuid: workspaceUUID,
                        name: modalRes.outputs.name,
                        color: modalRes.outputs.color,
                    },
                },
            });

            refetch();
        } catch (error) {
            console.error(error);
        }
    }
</script>

{#if $res.loading}
    <div class="flex min-h-[200px] items-center justify-center">
        <Loading />
    </div>
{:else}
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
{/if}

<DialogModal id="newLabel">
    <ConfirmModalContent
        title={$_("create-new-label")}
        confirmLabel={$_("Save")}
        inputs={[
            {
                name: "name",
                label: $_("name"),
                placeholder: $_("please-enter-a-label-name"),
                validation: {
                    required: true,
                },
            },
            {
                type: "colorPicker",
                name: "color",
                label: $_("color"),
                placeholder: $_("please-enter-a-label-color"),
                value: 0,
            },
        ]}
    />
</DialogModal>

<DialogModal id="editLabel">
    <ConfirmModalContent
        title={$_("edit-label")}
        confirmLabel={$_("Save")}
        inputs={[
            {
                name: "name",
                label: $_("name"),
                placeholder: $_("please-enter-a-label-name"),
                validation: {
                    required: true,
                },
            },
            {
                type: "colorPicker",
                name: "color",
                label: $_("color"),
                placeholder: $_("please-enter-a-label-color"),
                value: 0,
            },
        ]}
    />
</DialogModal>

<DialogModal id="deleteLabel">
    <ConfirmModalContent
        title={$_("delete-label")}
        confirmLabel={$_("Delete")}
        confirmColor="accent"
    >
        {$_("are-you-sure-you-want-to-delete-this-label")}
    </ConfirmModalContent>
</DialogModal>
