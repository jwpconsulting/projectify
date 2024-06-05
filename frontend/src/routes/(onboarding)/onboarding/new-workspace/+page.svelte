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
    import { _ } from "svelte-i18n";

    import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import { currentUser } from "$lib/stores/user";
    import { getNewProjectUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";
    import { openApiClient } from "$lib/repository/util";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import type { FormViewState } from "$lib/types/ui";

    export let data: PageData;
    const { workspace } = data;

    let state: FormViewState = { kind: "start" };
    let workspaceTitle: string | undefined = undefined;
    let workspaceTitleValidation: InputFieldValidation | undefined = undefined;

    $: disabled = workspaceTitle === undefined;

    $: who = $currentUser?.preferred_name ?? data.user.preferred_name;

    async function submit() {
        if (!workspaceTitle) {
            throw new Error("Exepcted workspaceTitle");
        }
        state = { kind: "submitting" };

        const { data, error } = await openApiClient.POST(
            "/workspace/workspace/",
            { body: { title: workspaceTitle } },
        );
        if (error === undefined) {
            const { uuid } = data;

            const nextStep = getNewProjectUrl(uuid);
            await goto(nextStep);
            return;
        }
        workspaceTitleValidation = error.details.title
            ? { ok: false, error: error.details.title }
            : {
                  ok: true,
                  result: $_("onboarding.new-workspace.fields.title.valid"),
              };
        if (workspaceTitleValidation.ok) {
            state = {
                kind: "error",
                message: $_("onboarding.new-workspace.errors.general"),
            };
        } else {
            state = {
                kind: "error",
                message: $_("onboarding.new-workspace.errors.fields"),
            };
        }
    }
</script>

<Onboarding nextAction={{ kind: "submit", disabled, submit }}>
    <svelte:fragment slot="title">
        {#if who}
            {$_("onboarding.new-workspace.title.with-name", {
                values: { who },
            })}
        {:else}
            {$_("onboarding.new-workspace.title.without-name", {})}
        {/if}
    </svelte:fragment>
    <svelte:fragment slot="prompt">
        {#if workspace}
            <p>{$_("onboarding.new-workspace.has-workspace")}</p>
            <p>
                <Anchor
                    size="large"
                    href={getNewProjectUrl(workspace.uuid)}
                    label={"Create project"}
                />
            </p>
        {:else}
            <p>{$_("onboarding.new-workspace.prompt")}</p>
        {/if}
    </svelte:fragment>
    <svelte:fragment slot="inputs">
        <InputField
            style={{ inputType: "text" }}
            name="workspaceTitle"
            label={$_("onboarding.new-workspace.fields.title.label")}
            placeholder={$_(
                "onboarding.new-workspace.fields.title.placeholder",
            )}
            bind:value={workspaceTitle}
            required
            validation={workspaceTitleValidation}
        />
        {#if state.kind === "error"}<p>{state.message}</p>{/if}
    </svelte:fragment>
    <DashboardPlaceholder
        slot="content"
        state={{
            kind: "new-workspace",
            workspace,
            title:
                workspaceTitle ?? $_("onboarding.new-workspace.default-name"),
        }}
    />
</Onboarding>
