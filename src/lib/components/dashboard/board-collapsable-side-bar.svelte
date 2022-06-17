<script lang="ts">
    import { _ } from "svelte-i18n";

    import DropDownMenu from "../dropDownMenu.svelte";
    import IconArchive from "../icons/icon-archive.svelte";
    import IconMenu from "../icons/icon-menu.svelte";
    import IconSettings from "../icons/icon-settings.svelte";
    import BoardsSideNav from "./boards-side-nav.svelte";

    export let selectedWorkspace;
    export let selectedWorkspaceUUID;
    export let selectedBoardUUID;
</script>

<nav
    class="sticky top-0 flex min-h-full w-60 shrink-0 flex-col overflow-hidden bg-base-100"
>
    <!-- Tite and settings -->
    <div class="sticky top-0 z-50 flex bg-base-100 p-4">
        <h1 class="grow text-xl font-bold capitalize">
            {selectedWorkspace ? selectedWorkspace.title : ""}
        </h1>
        <DropDownMenu
            items={[
                {
                    label: $_("Archive"),
                    icon: IconArchive,
                    href: `/dashboard/archive/${selectedWorkspaceUUID}`,
                },
                {
                    label: $_("settings"),
                    icon: IconSettings,
                    href: `/dashboard/settings/${selectedWorkspaceUUID}`,
                },
            ]}
        >
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label
                tabindex="0"
                class="btn btn-outline btn-primary btn-circle btn-xs"
            >
                <IconMenu />
            </label>
        </DropDownMenu>
    </div>

    <!-- Boards nav -->
    <div class="flex grow flex-col overflow-hidden">
        {#if selectedWorkspaceUUID}
            <h2 class="p-4 text-base font-bold">Workspace Boards</h2>
            <BoardsSideNav {selectedWorkspaceUUID} {selectedBoardUUID} />
        {/if}
    </div>
</nav>
