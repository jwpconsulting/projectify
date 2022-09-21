<script lang="ts">
    import DestructiveOverlay from "$lib/figma/DestructiveOverlay.svelte";
    import ContextMenu from "$lib/figma/ContextMenu.svelte";
    import { setFirstWorkspace } from "$lib/stores/dashboard";
    import type { ContextMenuType, DestructiveOverlayType } from "$lib/types";
    import { browser } from "$app/env";
    import { fc } from "$lib/storybook";

    const destructiveOverlays: DestructiveOverlayType[] = [
        {
            kind: "deleteLabel" as const,
            label: { name: "This is a label", color: 0, uuid: "" },
        },
        {
            kind: "deleteMember" as const,
            workspaceUser: {
                user: {
                    email: "hello@example.com",
                    full_name: "Firstname Lastname",
                },
                uuid: "",
                role: "",
                created: "",
                modified: "",
            },
        },
        {
            kind: "deleteSection" as const,
            workspaceBoardSection: {
                title: "section name",
                created: "",
                modified: "",
                uuid: "",
                _order: 0,
            },
        },
        {
            kind: "deleteTask" as const,
            task: {
                title: "task name",
                created: "",
                modified: "",
                uuid: "",
                _order: 0,
                number: 1,
                labels: [],
            },
        },
        {
            kind: "deleteSelectedTasks" as const,
            tasks: [
                {
                    title: "task name",
                    created: "",
                    modified: "",
                    uuid: "",
                    _order: 0,
                    number: 1,
                    labels: [],
                },
            ],
        },
        {
            kind: "archiveBoard" as const,
            workspaceBoard: {
                title: "board name",
                created: "",
                modified: "",
                uuid: "",
            },
        },
    ];

    const workspace = {
        uuid: "",
        title: "This is a workspace",
        created: "",
        modified: "",
    };
    const workspaceBoard = {
        title: "board name",
        created: "",
        modified: "",
        uuid: "",
    };
    const workspaceBoardSection = {
        title: "workspace board section",
        created: "",
        modified: "",
        uuid: "",
        _order: 0,
    };
    const task = {
        title: "this is a task",
        created: "",
        modified: "",
        uuid: "",
        _order: 0,
        labels: [],
        number: 1,
    };

    let contextMenus: ContextMenuType[] = [
        {
            kind: "profile" as const,
        },
        {
            kind: "workspace" as const,
        },
        {
            kind: "sideNav" as const,
            workspace,
        },
        {
            kind: "workspaceBoard" as const,
            workspaceBoard,
        },
        {
            kind: "workspaceBoardSection" as const,
            workspaceBoardSection,
        },
        {
            kind: "task" as const,
            task,
            location: "dashboard",
        },
        {
            kind: "task" as const,
            task,
            location: "task",
        },
        {
            kind: "help",
        },
        {
            kind: "permissions",
        },
    ];

    if (browser) {
        setFirstWorkspace();
    }
</script>

{#each destructiveOverlays as target}
    <DestructiveOverlay {target} />
{/each}

{#if browser}
    <div class={fc}>
        {#each contextMenus as target}
            <ContextMenu {target} />
        {/each}
    </div>
{/if}
