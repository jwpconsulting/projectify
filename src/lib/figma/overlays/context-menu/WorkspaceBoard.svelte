<script lang="ts">
    import { Archive, Pencil } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import { archiveWorkspaceBoard as repoArchiveWorkspaceBoard } from "$lib/repository/workspace/workspaceBoard";
    import {
        openConstructiveOverlay,
        openDestructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { WorkspaceBoard } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoard;

    async function editBoard() {
        await openConstructiveOverlay({
            kind: "updateWorkspaceBoard",
            workspaceBoard,
        });
    }

    async function archiveWorkspaceBoard() {
        // XXX this gives off a bit of a smell, because we accidentally
        // involve the context menu itself in a stack trace when the overlay
        // is cancelled:
        /* Uncaught (in promise) Error: Overlay was cancelled
         *     closeOverlay globalUi.ts:85
         *     update index.js:69
         *     closeOverlay globalUi.ts:73
         *     rejectDestructiveOverlay globalUi.ts:117
         *     dispose Button.svelte:129
         *     prevent_default dom.js:369
         *     listen dom.js:359
         *     listen_dev dev.js:133
         *     mount Button.svelte:158
         *     mount Button.svelte:987
         *     m svelte-hooks.js:291
         *     mount_component Component.js:44
         *     mount DestructiveOverlay.svelte:171
         *     m svelte-hooks.js:291
         *     mount_component Component.js:44
         *     mount +layout.svelte:239
         *     mount OverlayContainer.svelte:144
         *     update OverlayContainer.svelte:294
         *     update scheduler.js:119
         *     flush scheduler.js:79
         *     promise callback*schedule_update scheduler.js:20
         *     make_dirty Component.js:81
         *     ctx Component.js:129
         *     instance ContextMenuContainer.svelte:236
         *     set index.js:56
         *     update index.js:69
         *     closeOverlay globalUi.ts:73
         *     closeContextMenu globalUi.ts:178
         *     action ContextMenuButton.svelte:34
         *     listen dom.js:359
         *     listen_dev dev.js:133
         *     mount ContextMenuButton.svelte:90
         *     mount ContextMenuButton.svelte:413
         *     m svelte-hooks.js:291
         *     mount_component Component.js:44
         *     mount WorkspaceBoard.svelte:83
         *     mount Layout.svelte:53
         *     m svelte-hooks.js:291
         *     mount_component Component.js:44
         *     mount WorkspaceBoard.svelte:146
         *     m svelte-hooks.js:291
         *     mount_component Component.js:44
         *     mount ContextMenu.svelte:359
         *     mount ContextMenu.svelte:587
         *     m svelte-hooks.js:291
         *     mount_component Component.js:44
         *     mount ContextMenuContainer.svelte:68
         *     update ContextMenuContainer.svelte:177
         *     update scheduler.js:119
         *     flush scheduler.js:79
         *     promise callback*schedule_update scheduler.js:20
         *     make_dirty Component.js:81
         *     ctx Component.js:129
         *     instance ContextMenuContainer.svelte:236
         *     set index.js:56
         *     update index.js:69
         *     openContextMenu globalUi.ts:156
         *     openContextMenu globalUi.ts:155
         *     toggleMenu SelectWorkspaceBoard.svelte:30
         *     dispose CircleIcon.svelte:43
         *     prevent_default dom.js:369
         *     stop_propagation dom.js:379
         *     listen dom.js:359
         *     listen_dev dev.js:133
         *     mount CircleIcon.svelte:205
         *     mount CircleIcon.svelte:292
         *     m svelte-hooks.js:291
         *     mount_component Component.js:44
         *     mount SelectWorkspaceBoard.svelte:151
         *     m svelte-hooks.js:291
         *     mount_component Component.js:44
         *     mount Boards.svelte:336
         *     mount Boards.svelte:241
         *     mount Boards.svelte:88
         *     mount Boards.svelte:410
         *     m svelte-hooks.js:291
         *     mount_component Component.js:44
         *     mount Full.svelte:102
         *     m svelte-hooks.js:291
         *     mount_component Component.js:44
         * globalUi.ts:85:28
         */
        // TODO move awaiting a closed context menu away from awaiting a
        // successful dialog. Reason: We should separate concerns here.
        await openDestructiveOverlay({
            kind: "archiveWorkspaceBoard",
            workspaceBoard,
        });
        await repoArchiveWorkspaceBoard(workspaceBoard, true, { fetch });
    }
</script>

<Layout>
    <ContextMenuButton
        kind={{
            kind: "button",
            action: editBoard,
        }}
        label={$_("overlay.context-menu.workspace-board.edit-board")}
        state="normal"
        icon={Pencil}
    />
    <ContextMenuButton
        kind={{
            kind: "button",
            action: archiveWorkspaceBoard,
        }}
        label={$_(
            "overlay.context-menu.workspace-board.archive-workspace-board",
        )}
        state="normal"
        icon={Archive}
    />
</Layout>
