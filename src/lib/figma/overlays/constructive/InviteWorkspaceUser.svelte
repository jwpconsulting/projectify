<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/figma/overlays/constructive/Layout.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { rejectConstructiveOverlay } from "$lib/stores/globalUi";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;
    console.log("TODO do something with", workspace);
</script>

<Layout>
    <svelte:fragment slot="title">
        {$_("overlay.constructive.invite-workspace-user.title")}
    </svelte:fragment>
    <svelte:fragment slot="form">
        <InputField
            name="workspace-board-name"
            label={$_(
                "overlay.constructive.invite-workspace-user.form.email.label"
            )}
            placeholder={$_(
                "overlay.constructive.invite-workspace-user.form.email.placeholder"
            )}
            style={{ kind: "field", inputType: "text" }}
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
