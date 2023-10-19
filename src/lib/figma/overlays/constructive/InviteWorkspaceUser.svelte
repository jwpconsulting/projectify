<script lang="ts">
    // TODO I should be called InviteUser - because we are inviting users
    // on Projectify to join this workspace as a workspace user...
    import { _ } from "svelte-i18n";

    import Layout from "$lib/figma/overlays/constructive/Layout.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { inviteUser } from "$lib/repository/workspace";
    import {
        rejectConstructiveOverlay,
        resolveConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;

    let email: string | undefined;

    async function onSubmit() {
        if (email === undefined) {
            throw new Error("No email");
        }
        await inviteUser(workspace, email);
        resolveConstructiveOverlay();
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
            style={{ kind: "field", inputType: "email" }}
            required
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
