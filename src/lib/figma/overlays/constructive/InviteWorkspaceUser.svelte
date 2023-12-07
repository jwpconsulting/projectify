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
                    "overlay.constructive.invite-workspace-user.form.email.validation.ok"
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
                "overlay.constructive.invite-workspace-user.form.email.label"
            )}
            placeholder={$_(
                "overlay.constructive.invite-workspace-user.form.email.placeholder"
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
