<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { WorkspaceBoard } from "$lib/types/workspace";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Folder } from "@steeze-ui/heroicons";
    import { getModal } from "$lib/components/dialogModal.svelte";
    import CircleIcon from "$lib/figma/CircleIcon.svelte";
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

    function selectBoard() {
        if (workspaceBoard.uuid === $currentWorkspaceBoardUuid) {
            console.log("Already here");
        } else {
            goto(getDashboardWorkspaceBoardUrl(workspaceBoard.uuid));
        }
    }
</script>

<button
    class="group flex w-full flex-row justify-between py-2 px-4 hover:bg-base-200"
    on:click={selectBoard}
>
    <div class="flex flex-row items-center gap-2">
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
        >
    </div>
    <div class="invisible group-hover:visible" bind:this={buttonRef}>
        <CircleIcon
            size="small"
            icon="ellipsis"
            disabled={false}
            on:click={toggleMenu}
        />
    </div>
</button>
