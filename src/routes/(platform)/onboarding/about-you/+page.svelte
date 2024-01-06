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

    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { goto } from "$lib/navigation";
    import { updateUserProfile } from "$lib/stores/user";
    import { newWorkspaceUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { user } = data;

    let fullName: string | undefined = user.full_name;

    $: disabled = fullName === undefined;

    async function submit() {
        if (fullName == undefined) {
            throw new Error("Expected fullName");
        }
        await updateUserProfile(fullName, { fetch });
        await goto(newWorkspaceUrl);
    }
</script>

<Onboarding nextAction={{ kind: "submit", disabled, submit }}>
    <svelte:fragment slot="title"
        >{$_("onboarding.about-you.title")}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        {$_("onboarding.about-you.prompt")}
    </svelte:fragment>
    <svelte:fragment slot="inputs">
        <InputField
            bind:value={fullName}
            label={$_("onboarding.about-you.input.label")}
            placeholder={$_("onboarding.about-you.input.placeholder")}
            style={{ inputType: "text" }}
            name="full-name"
            required
        />
    </svelte:fragment>

    <svelte:fragment slot="content">
        <h1 class="text-4xl font-bold">
            {#if fullName}
                {$_("onboarding.about-you.greeting.with-name", {
                    values: { name: fullName },
                })}
            {:else}
                {$_("onboarding.about-you.greeting.without-name")}
            {/if}
        </h1>
    </svelte:fragment>
</Onboarding>
