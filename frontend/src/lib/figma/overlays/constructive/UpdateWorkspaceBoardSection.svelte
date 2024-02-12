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
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { updateWorkspaceBoardSection } from "$lib/repository/workspace/workspaceBoardSection";
    import {
        rejectConstructiveOverlay,
        resolveConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { AuthViewState } from "$lib/types/ui";
    import type { WorkspaceBoardSection } from "$lib/types/workspace";

    export let workspaceBoardSection: WorkspaceBoardSection;

    let state: AuthViewState = { kind: "start" };

    let { title } = workspaceBoardSection;

    async function onSubmit() {
        state = { kind: "submitting" };
        const result = await updateWorkspaceBoardSection(
            { ...workspaceBoardSection, title },
            { fetch },
        );
        if (!result.ok) {
            // TODO show error
            state = { kind: "error", message: JSON.stringify(result.error) };
            throw result.error;
        }
        resolveConstructiveOverlay();
    }
</script>

<Layout {onSubmit}>
    <svelte:fragment slot="title">
        {$_("overlay.constructive.update-workspace-board-section.title")}
    </svelte:fragment>
    <svelte:fragment slot="form">
        <InputField
            name="workspace-board-name"
            label={$_(
                "overlay.constructive.update-workspace-board-section.form.title.label",
            )}
            placeholder={$_(
                "overlay.constructive.update-workspace-board-section.form.title.placeholder",
            )}
            style={{ inputType: "text" }}
            bind:value={title}
        />
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
            label={$_(
                "overlay.constructive.update-workspace-board-section.cancel",
            )}
        />
        <Button
            action={{ kind: "submit", disabled: state.kind === "submitting" }}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
            label={$_(
                "overlay.constructive.update-workspace-board-section.update",
            )}
        />
    </svelte:fragment>
</Layout>
