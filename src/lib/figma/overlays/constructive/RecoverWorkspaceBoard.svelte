<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/figma/overlays/constructive/Layout.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { archiveWorkspaceBoard } from "$lib/repository/workspace/workspaceBoard";
    import {
        rejectConstructiveOverlay,
        resolveConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { AuthViewState } from "$lib/types/ui";
    import type { WorkspaceBoard } from "$lib/types/workspace";

    export let workspaceBoard: WorkspaceBoard;

    let state: AuthViewState = { kind: "start" };

    async function onSubmit() {
        state = { kind: "submitting" };
        const result = await archiveWorkspaceBoard(workspaceBoard, false, {
            fetch,
        });
        if (!result.ok) {
            // TODO show error here
            state = { kind: "error", message: JSON.stringify(result.error) };
            throw result.error;
        }
        resolveConstructiveOverlay();
    }
</script>

<Layout {onSubmit}>
    <svelte:fragment slot="title">
        {$_("overlay.constructive.recover-workspace-board.title")}
    </svelte:fragment>
    <svelte:fragment slot="message">
        <p class="text-center text-error">
            {$_("overlay.constructive.recover-workspace-board.notice")}
        </p>
    </svelte:fragment>
    <svelte:fragment slot="buttons">
        <Button
            action={{
                kind: "button",
                action: rejectConstructiveOverlay,
                disabled: state.kind === "submitting",
            }}
            style={{ kind: "secondary" }}
            size="medium"
            color="blue"
            label={$_("overlay.constructive.recover-workspace-board.cancel")}
        />
        <Button
            action={{ kind: "submit", disabled: state.kind === "submitting" }}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
            label={$_(
                "overlay.constructive.recover-workspace-board.recover-board",
            )}
        />
    </svelte:fragment>
</Layout>
