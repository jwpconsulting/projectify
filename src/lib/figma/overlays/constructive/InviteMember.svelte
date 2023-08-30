<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { rejectConstructiveOverlay } from "$lib/stores/globalUi";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;
    console.log("TODO do something with", workspace);
</script>

<div class="flex flex-col gap-2">
    <InputField
        name="workspace-board-name"
        label={$_("invite-member.enter-email-address")}
        placeholder={$_("invite-member.enter-an-email")}
        style={{ kind: "field", inputType: "text" }}
    />
</div>
<div class="flex flex-row justify-center">
    <Button
        action={{
            kind: "button",
            action: rejectConstructiveOverlay,
        }}
        style={{ kind: "secondary" }}
        size="medium"
        color="blue"
        label={$_("edit-workspace-board.cancel")}
    />
    <Button
        action={{
            kind: "button",
            action: console.error.bind(null, "Invite not implemented"),
        }}
        style={{ kind: "primary" }}
        size="medium"
        color="blue"
        label={$_("invite-member.invite")}
    />
</div>
