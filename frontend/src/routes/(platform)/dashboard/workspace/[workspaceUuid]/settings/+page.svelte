<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023-2024 JWP Consulting GK

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
    import type { BeforeNavigate } from "@sveltejs/kit";
    import { _ } from "svelte-i18n";

    import vars from "$lib/env";
    import UploadAvatar from "$lib/figma/buttons/UploadAvatar.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { updateWorkspace } from "$lib/repository/workspace";
    import { currentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import type { EditableViewState } from "$lib/types/ui";
    import { uploadImage } from "$lib/utils/file";

    import type { PageData } from "./$types";

    import { beforeNavigate } from "$app/navigation";

    export let data: PageData;

    let { workspace } = data;

    const uuid = workspace.uuid;

    let { title, description, picture } = workspace;

    let state: EditableViewState = { kind: "viewing" };

    $: canEdit = $currentTeamMemberCan("update", "workspace");

    function resetForm() {
        title = workspace.title;
        description = workspace.description;
    }

    function fieldChanged() {
        state = { kind: "editing" };
    }

    function removePicture() {
        state = { kind: "editing" };
        imageFile = undefined;
        picture = null;
    }

    let imageFile: File | undefined = undefined;
    $: hasImage = imageFile !== undefined || picture !== null;

    function fileSelected(file: File, src: string) {
        state = { kind: "editing" };
        imageFile = file;
        picture = src;
    }

    async function save() {
        state = { kind: "saving" };
        await uploadImage(
            imageFile,
            vars.API_ENDPOINT + `/workspace/workspace/${uuid}/picture-upload`,
        );
        const result = await updateWorkspace(uuid, title, description, {
            fetch,
        });
        workspace = {
            ...workspace,
            ...result,
        };
        resetForm();
        state = { kind: "viewing" };
    }

    function cancel() {
        state = { kind: "viewing" };
        resetForm();
    }

    beforeNavigate((navigation: BeforeNavigate) => {
        if (state.kind == "editing") {
            const navigateAway = window.confirm(
                $_("workspace-settings.general.confirm-navigate-away"),
            );
            if (!navigateAway) {
                navigation.cancel();
            }
        }
    });
</script>

<svelte:head>
    <title
        >{$_("workspace-settings.title", {
            values: { title: workspace.title },
        })}</title
    >
</svelte:head>

<form
    class="flex flex-col gap-6"
    on:submit|preventDefault={save}
    name="general"
>
    <div class="flex flex-col items-center">
        <div class="relative flex h-24 w-24 w-max flex-col">
            {#if picture}
                <img
                    src={picture}
                    class="h-full"
                    alt={$_("workspace-settings.general.picture.alt")}
                />
            {:else}
                <div class="h-24 w-24">
                    {$_("workspace-settings.general.picture.no-picture")}
                </div>
            {/if}
            {#if canEdit}
                <div class="absolute -bottom-1/4 -right-1/4">
                    <UploadAvatar
                        label={$_("workspace-settings.general.picture.label")}
                        {fileSelected}
                    />
                </div>
            {/if}
        </div>
    </div>
    <div class="flex flex-col gap-6">
        <InputField
            bind:value={title}
            placeholder={$_(
                "workspace-settings.general.workspace-name.placeholder",
            )}
            onClick={canEdit ? fieldChanged : undefined}
            style={{ inputType: "text" }}
            name="title"
            label={$_("workspace-settings.general.workspace-name.label")}
            readonly={!canEdit || state.kind !== "editing"}
        />
        <InputField
            bind:value={description}
            placeholder={$_(
                "workspace-settings.general.description.placeholder",
            )}
            onClick={canEdit ? fieldChanged : undefined}
            style={{ inputType: "text" }}
            name="title"
            label={$_("workspace-settings.general.description.label")}
            readonly={!canEdit || state.kind !== "editing"}
        />
        {#if canEdit}
            <Button
                action={{
                    kind: "button",
                    action: removePicture,
                    disabled: !hasImage || state.kind === "saving",
                }}
                size="medium"
                style={{ kind: "secondary" }}
                color="blue"
                label={$_("workspace-settings.general.picture.remove-picture")}
            />
            <Button
                action={{
                    kind: "submit",
                    disabled: state.kind !== "editing",
                }}
                size="medium"
                style={{ kind: "primary" }}
                color="blue"
                label={$_("workspace-settings.general.save")}
            />
            <Button
                action={{
                    kind: "button",
                    action: cancel,
                    disabled: state.kind !== "editing",
                }}
                size="medium"
                style={{ kind: "secondary" }}
                color="blue"
                label={$_("workspace-settings.general.cancel")}
            />
        {/if}
    </div>
</form>
{#if $currentTeamMemberCan("delete", "workspace")}
    <section class="flex flex-col gap-2">
        <h2 class="font-bold">
            {$_("workspace-settings.general.delete.title")}
        </h2>

        <p>
            {$_("workspace-settings.general.delete.message")}
        </p>
        <Anchor
            label={$_("workspace-settings.general.delete.label")}
            href={$_("workspace-settings.general.delete.email")}
        />
    </section>
{/if}
