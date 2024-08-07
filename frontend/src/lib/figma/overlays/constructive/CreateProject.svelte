<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023, 2024 JWP Consulting GK

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
    import { goto } from "$lib/navigation";
    import {
        rejectConstructiveOverlay,
        resolveConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { FormViewState } from "$lib/types/ui";
    import type { WorkspaceDetail } from "$lib/types/workspace";
    import { getDashboardProjectUrl } from "$lib/urls";
    import { openApiClient } from "$lib/repository/util";

    export let workspace: Pick<WorkspaceDetail, "uuid">;

    let state: FormViewState = { kind: "start" };

    let title: string | undefined = undefined;

    async function onSubmit() {
        state = { kind: "submitting" };
        if (!title) {
            throw new Error("Not valid");
        }
        const { data, error } = await openApiClient.POST(
            "/workspace/project/",
            {
                body: {
                    workspace_uuid: workspace.uuid,
                    title,
                    description: null,
                },
            },
        );
        if (data) {
            await goto(getDashboardProjectUrl(data));
            resolveConstructiveOverlay();
        } else {
            // TODO format error
            state = {
                kind: "error",
                message: JSON.stringify(error),
            };
        }
    }
</script>

<Layout {onSubmit}>
    <svelte:fragment slot="title">
        {$_("overlay.constructive.create-project.title")}
    </svelte:fragment>
    <svelte:fragment slot="form">
        <InputField
            name="project-name"
            label={$_("overlay.constructive.create-project.form.title.label")}
            placeholder={$_(
                "overlay.constructive.create-project.form.title.placeholder",
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
            label={$_("overlay.constructive.create-project.cancel")}
        />
        <Button
            action={{ kind: "submit", disabled: state.kind === "submitting" }}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
            label={$_("overlay.constructive.create-project.create")}
        />
    </svelte:fragment>
</Layout>
