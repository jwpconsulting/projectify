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
    import { goto } from "$lib/navigation";
    import {
        rejectConstructiveOverlay,
        resolveConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { FormViewState } from "$lib/types/ui";
    import type { WorkspaceDetailProject } from "$lib/types/workspace";
    import { getDashboardProjectUrl } from "$lib/urls";
    import { openApiClient } from "$lib/repository/util";

    export let project: WorkspaceDetailProject;

    let state: FormViewState = { kind: "start" };

    async function onSubmit() {
        state = { kind: "submitting" };
        const { error } = await openApiClient.POST(
            "/workspace/project/{project_uuid}/archive",
            {
                params: { path: { project_uuid: project.uuid } },
                body: { archived: false },
            },
        );
        if (error === undefined) {
            resolveConstructiveOverlay();
            await goto(getDashboardProjectUrl(project));
        } else {
            state = {
                kind: "error",
                message: $_("overlay.constructive.recover-project.error", {
                    values: { details: JSON.stringify(error) },
                }),
            };
        }
    }
</script>

<Layout {onSubmit}>
    <svelte:fragment slot="title">
        {$_("overlay.constructive.recover-project.title", {
            values: { title: project.title },
        })}
    </svelte:fragment>
    <svelte:fragment slot="message">
        <p class="text-center">
            {$_("overlay.constructive.recover-project.notice")}
        </p>
        {#if state.kind === "error"}
            <p>
                {state.message}
            </p>
        {/if}
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
            label={$_("overlay.constructive.recover-project.cancel")}
        />
        <Button
            action={{ kind: "submit", disabled: state.kind === "submitting" }}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
            label={state.kind === "submitting"
                ? $_("overlay.constructive.recover-project.submit.submitting")
                : $_("overlay.constructive.recover-project.submit.start")}
        />
    </svelte:fragment>
</Layout>
