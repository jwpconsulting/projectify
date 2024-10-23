<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/figma/overlays/constructive/Layout.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import {
        rejectConstructiveOverlay,
        resolveConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { FormViewState } from "$lib/types/ui";
    import type { WorkspaceDetailProject } from "$lib/types/workspace";
    import { openApiClient } from "$lib/repository/util";

    export let project: WorkspaceDetailProject;

    let state: FormViewState = { kind: "start" };

    let title = project.title;

    async function onSubmit() {
        state = { kind: "submitting" };
        const { error } = await openApiClient.PUT(
            "/workspace/project/{project_uuid}",
            {
                params: { path: { project_uuid: project.uuid } },
                body: { ...project, title },
            },
        );
        if (error) {
            // TODO format error
            state = {
                kind: "error",
                message: JSON.stringify(error),
            };
        } else {
            resolveConstructiveOverlay();
        }
    }
</script>

<Layout {onSubmit}>
    <svelte:fragment slot="title">
        {$_("overlay.constructive.update-project.title")}
    </svelte:fragment>
    <svelte:fragment slot="form">
        <InputField
            label={$_("overlay.constructive.update-project.form.title.label")}
            name="project-name"
            placeholder={$_(
                "overlay.constructive.update-project.form.title.placeholder",
            )}
            style={{ inputType: "text" }}
            bind:value={title}
            required
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
            label={$_("overlay.constructive.update-project.cancel")}
        />
        <Button
            action={{
                kind: "submit",
                disabled: state.kind === "submitting",
            }}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
            label={$_("overlay.constructive.update-project.save")}
        />
    </svelte:fragment>
</Layout>
