<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
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
