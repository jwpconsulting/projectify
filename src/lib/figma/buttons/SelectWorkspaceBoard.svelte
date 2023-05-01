<script lang="ts">
    import { Icon } from "@steeze-ui/svelte-icon";
    import { Folder } from "@steeze-ui/heroicons";
    import type { WorkspaceBoard } from "$lib/types/workspace";
    import CircleIcon from "$lib/figma/buttons/CircleIcon.svelte";
    import { getDashboardWorkspaceBoardUrl } from "$lib/urls";

    import type { WorkspaceBoardSearchModule } from "$lib/types/stores";
    // import { goto } from "$app/navigation";

    export let workspaceBoardSearchModule: WorkspaceBoardSearchModule;
    export let workspaceBoard: WorkspaceBoard;

    let { currentWorkspaceBoardUuid } = workspaceBoardSearchModule;

    let buttonRef: HTMLElement;

    function toggleMenu() {
        // TODO context menu
        console.error("TODO use", buttonRef);
    }
</script>

<a
    class="group block flex w-full flex-row justify-between py-2 px-4 hover:bg-base-200"
    href={getDashboardWorkspaceBoardUrl(workspaceBoard.uuid)}
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
            action={{ kind: "button", action: toggleMenu }}
        />
    </div>
</a>
