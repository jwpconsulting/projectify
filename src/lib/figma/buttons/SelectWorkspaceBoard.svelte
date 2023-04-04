<script lang="ts">
    import type { WorkspaceBoard } from "$lib/types/workspace";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Folder } from "@steeze-ui/heroicons";
    import CircleIcon from "$lib/figma/buttons/CircleIcon.svelte";
    import { Mutation_ArchiveWorkspaceBoard } from "$lib/graphql/operations";
    import { client } from "$lib/graphql/client";

    import type { WorkspaceBoardSearchModule } from "$lib/types/stores";
    // import { goto } from "$app/navigation";

    export let workspaceBoardSearchModule: WorkspaceBoardSearchModule;
    export let workspaceBoard: WorkspaceBoard;

    let { currentWorkspaceBoardUuid, currentWorkspaceBoard } =
        workspaceBoardSearchModule;

    let buttonRef: HTMLElement;

    async function onEdit() {
        // TODO modal
        // await client.mutate({
        //     mutation: Mutation_UpdateWorkspaceBoard,
        //     variables: {
        //         input: {
        //             uuid: workspaceBoard.uuid,
        //             title: modalRes.outputs.title,
        //             deadline: modalRes.outputs.deadline,
        //             description: "",
        //         },
        //     },
        // });
    }

    async function onArchive() {
        // TODO confirmation dialog
        await client.mutate({
            mutation: Mutation_ArchiveWorkspaceBoard,
            variables: {
                input: {
                    uuid: workspaceBoard.uuid,
                    archived: true,
                },
            },
        });

        // TODO here we ought to find out the URL of the workspace this
        // workspace board belongs to
        console.error("TODO");
    }

    function toggleMenu() {
        // TODO context menu
    }

    function selectBoard() {
        if (workspaceBoard.uuid === $currentWorkspaceBoardUuid) {
            console.log("Already here");
        } else {
            // TODO
            // goto(getDashboardWorkspaceBoardUrl(workspaceBoard.uuid));
        }
    }
</script>

<button
    class="group flex w-full flex-row justify-between py-2 px-4 hover:bg-base-200"
    on:click={selectBoard}
>
    <div class="flex min-w-0 flex-row items-center gap-2">
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
        <div class="nowrap-ellipsis text-xs font-bold">
            {workspaceBoard.title}
        </div>
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
