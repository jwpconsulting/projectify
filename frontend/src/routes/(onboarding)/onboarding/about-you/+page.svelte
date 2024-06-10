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

    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { goto } from "$lib/navigation";
    import { currentUser, updateUserProfile } from "$lib/stores/user";
    import { aboutYouUrl, newWorkspaceUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import type { FormViewState } from "$lib/types/ui";
    import { getLogInWithNextUrl } from "$lib/urls/user";

    export let data: PageData;

    let state: FormViewState = { kind: "start" };
    let preferredName: PageData["user"]["preferred_name"] =
        $currentUser.kind === "authenticated"
            ? $currentUser.preferred_name
            : data.user.preferred_name;
    let preferredNameValidation: InputFieldValidation | undefined = undefined;

    async function submit() {
        state = { kind: "submitting" };
        const { error, data } = await updateUserProfile(preferredName);
        if (data) {
            await goto(newWorkspaceUrl);
            return;
        }
        if (error.code === 500) {
            state = {
                kind: "error",
                message: $_("onboarding.about-you.errors.server", {
                    values: { error: JSON.stringify(error) },
                }),
            };
            return;
        }
        if (error.code === 403) {
            await goto(getLogInWithNextUrl(aboutYouUrl));
            return;
        }
        const { details } = error;
        preferredNameValidation = details.preferred_name
            ? { ok: false, error: details.preferred_name }
            : undefined;
        state = {
            kind: "error",
            message: $_("onboarding.about-you.errors.fields"),
        };
    }
</script>

<svelte:head><title>{$_("onboarding.about-you.title")}</title></svelte:head>

<Onboarding
    nextAction={{
        kind: "submit",
        submit: submit,
        disabled: state.kind === "submitting",
    }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.about-you.heading")}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        {$_("onboarding.about-you.prompt")}
    </svelte:fragment>
    <svelte:fragment slot="inputs">
        <InputField
            bind:value={preferredName}
            label={$_("onboarding.about-you.input.label")}
            placeholder={$_("onboarding.about-you.input.placeholder")}
            style={{ inputType: "text" }}
            name="full-name"
            validation={preferredNameValidation}
        />
        {#if state.kind === "error"}
            <p>{state.message}</p>
        {/if}
    </svelte:fragment>

    <svelte:fragment slot="content">
        <h1
            class="w-full overflow-hidden text-ellipsis text-center text-4xl font-bold"
        >
            {#if preferredName !== null && preferredName !== ""}
                {$_("onboarding.about-you.greeting.with-name", {
                    values: { name: preferredName },
                })}
            {:else}
                {$_("onboarding.about-you.greeting.without-name")}
            {/if}
        </h1>
    </svelte:fragment>
</Onboarding>
