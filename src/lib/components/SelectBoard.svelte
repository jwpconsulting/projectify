<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { WorkspaceBoard } from "$lib/types";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Folder, DotsHorizontal } from "@steeze-ui/heroicons";
    import { getModal } from "$lib/components/dialogModal.svelte";
    import {
        Mutation_UpdateWorkspaceBoard,
        Mutation_ArchiveWorkspaceBoard,
    } from "$lib/graphql/operations";
    import { client } from "$lib/graphql/client";
    import { currentWorkspaceBoardUuid } from "$lib/stores/dashboard";
    import { getDashboardWorkspaceUrl } from "$lib/urls";
    import { getDashboardWorkspaceBoardUrl } from "$lib/urls";
    import { getDropDown } from "$lib/components/globalDropDown.svelte";
    import type { DropDownMenuItem } from "$lib/components/globalDropDown.svelte";
    import { goto } from "$app/navigation";
    import {
        currentWorkspace,
        currentWorkspaceBoard,
    } from "$lib/stores/dashboard";

    export let workspaceBoard: WorkspaceBoard;
    let buttonRef: HTMLElement;
    let dropDownItems: DropDownMenuItem[];

    async function onEdit() {
        let modalRes = await getModal("editBoardModal").open(workspaceBoard);

        if (!modalRes) {
            return;
        }
        console.log(modalRes);
        console.log(modalRes.outputs.title);

        await client.mutate({
            mutation: Mutation_UpdateWorkspaceBoard,
            variables: {
                input: {
                    uuid: workspaceBoard.uuid,
                    title: modalRes.outputs.title,
                    deadline: modalRes.outputs.deadline,
                    description: "",
                },
            },
        });
    }

    async function onArchive() {
        let modalRes = await getModal("archiveBoardConfirmModal").open();

        if (!modalRes) {
            return;
        }

        await client.mutate({
            mutation: Mutation_ArchiveWorkspaceBoard,
            variables: {
                input: {
                    uuid: workspaceBoard.uuid,
                    archived: true,
                },
            },
        });

        if ($currentWorkspaceBoard) {
            if ($currentWorkspaceBoard.uuid == workspaceBoard.uuid) {
                if (!$currentWorkspace) {
                    throw new Error("Expected $currentWorkspace");
                }
                goto(getDashboardWorkspaceUrl($currentWorkspace.uuid));
            }
        } else {
            throw new Error("Expected $currentWorkspaceBoard");
        }
    }

    $: {
        dropDownItems = [
            {
                label: $_("select-board.edit-board"),
                icon: null,
                onClick: onEdit,
            },
            {
                label: $_("select-board.archive-board"),
                icon: null,
                onClick: onArchive,
            },
        ];
    }

    function toggleMenu() {
        const dropDown = getDropDown();
        if (!dropDown) {
            throw new Error("Expected dropDown");
        }
        dropDown.open(dropDownItems, buttonRef, {
            dispatch: () => {
                if (!dropDown) {
                    throw new Error("Expected dropDown");
                }
                dropDown.close();
            },
        });
    }
</script>

<div class="group flex flex-row justify-between py-2 px-4 hover:bg-base-200">
    <a
        class="flex flex-row items-center gap-2"
        href={getDashboardWorkspaceBoardUrl(workspaceBoard.uuid)}
    >
        <div
            class={`rounded-md p-1 ${
                workspaceBoard.uuid === $currentWorkspaceBoardUuid
                    ? "bg-primary-focus"
                    : ""
            }`}
        >
            <Icon
                src={Folder}
                theme="outline"
                class={`h-4 w-4 ${
                    workspaceBoard.uuid === $currentWorkspaceBoardUuid
                        ? "text-base-100"
                        : ""
                }`}
            />
        </div>
        <span class="nowrap-ellipsis text-xs font-bold capitalize"
            >{workspaceBoard.title}</span
        ></a
    >
    <button
        class="flex h-6 w-6 flex-row p-1"
        on:click={toggleMenu}
        bind:this={buttonRef}
    >
        <Icon
            src={DotsHorizontal}
            theme="outline"
            class="h-4 w-4 text-base-100 group-hover:text-base-content"
        />
    </button>
</div>
