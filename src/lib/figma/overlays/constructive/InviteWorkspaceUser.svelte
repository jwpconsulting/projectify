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
    // TODO I should be called InviteUser - because we are inviting users
    // on Projectify to join this workspace as a workspace user...
    import { _ } from "svelte-i18n";

    import Layout from "$lib/figma/overlays/constructive/Layout.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { InputFieldValidation } from "$lib/funabashi/types";
    import { inviteUser } from "$lib/repository/workspace";
    import {
        rejectConstructiveOverlay,
        resolveConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;

    let email: string | undefined;
    let validation: InputFieldValidation | undefined = undefined;

    async function onSubmit() {
        if (email === undefined) {
            throw new Error("No email");
        }
        const result = await inviteUser(workspace, email, { fetch });
        if (result.ok) {
            validation = {
                ok: true,
                result: $_(
                    "overlay.constructive.invite-workspace-user.form.email.validation.ok",
                ),
            };
            resolveConstructiveOverlay();
        } else {
            validation = { ok: false, error: result.error.email };
        }
    }
</script>

<Layout {onSubmit}>
    <svelte:fragment slot="title">
        {$_("overlay.constructive.invite-workspace-user.title")}
    </svelte:fragment>
    <svelte:fragment slot="form">
        <InputField
            name="workspace-board-name"
            bind:value={email}
            label={$_(
                "overlay.constructive.invite-workspace-user.form.email.label",
            )}
            placeholder={$_(
                "overlay.constructive.invite-workspace-user.form.email.placeholder",
            )}
            style={{ inputType: "email" }}
            required
            {validation}
        />
    </svelte:fragment>
    <svelte:fragment slot="buttons">
        <Button
            action={{
                kind: "button",
                action: rejectConstructiveOverlay,
            }}
            style={{ kind: "secondary" }}
            size="medium"
            color="blue"
            label={$_("overlay.constructive.invite-workspace-user.cancel")}
        />
        <Button
            action={{ kind: "submit" }}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
            label={$_("overlay.constructive.invite-workspace-user.invite")}
        />
    </svelte:fragment>
</Layout>
