<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023, 2024 JWP Consulting GK -->
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
