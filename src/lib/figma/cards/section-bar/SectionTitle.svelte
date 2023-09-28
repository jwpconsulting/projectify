<script lang="ts">
    import { ChevronDown, ChevronRight } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";

    import { getNewTaskUrl } from "$lib/urls";

    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";
    import { toggleWorkspaceBoardSectionOpen } from "$lib/stores/dashboard";
    import { openContextMenu } from "$lib/stores/globalUi";
    import type { ContextMenuType } from "$lib/types/ui";
    import type {
        WorkspaceBoard,
        WorkspaceBoardSection,
    } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoard;
    export let workspaceBoardSection: WorkspaceBoardSection;
    export let open: boolean;

    const { uuid } = workspaceBoardSection;
    $: toggleOpen = toggleWorkspaceBoardSectionOpen.bind(null, uuid);
    let dropDownMenuBtnRef: HTMLElement;

    async function openDropDownMenu() {
        // TODO
        console.log("Need to open drop down menu at", dropDownMenuBtnRef);
        const contextMenuType: ContextMenuType = {
            kind: "workspaceBoardSection",
            workspaceBoard,
            workspaceBoardSection,
        };
        await openContextMenu(contextMenuType, dropDownMenuBtnRef);
    }
</script>

<header
    class="flex w-full flex-row items-center justify-between bg-foreground px-4 py-2"
>
    <div
        data-figma-name="Section header"
        class="flex min-w-0 shrink flex-row gap-4 text-base-content"
    >
        <button on:click={toggleOpen}>
            <Icon
                src={open ? ChevronDown : ChevronRight}
                class="h-6 w-6"
                theme="outline"
            />
        </button>
        <h1 class="nowrap-ellipsis min-w-0 shrink font-bold uppercase">
            {workspaceBoardSection.title}
        </h1>
    </div>
    <div class="flex shrink-0 flex-row gap-6" data-figma-name="Right side">
        <SquovalIcon
            action={{
                kind: "a",
                href: getNewTaskUrl(workspaceBoardSection.uuid),
            }}
            icon="plus"
            state="active"
            active={false}
        />
        <div bind:this={dropDownMenuBtnRef}>
            <SquovalIcon
                icon="ellipsis"
                state="active"
                active={false}
                action={{ kind: "button", action: openDropDownMenu }}
            />
        </div>
    </div>
</header>
