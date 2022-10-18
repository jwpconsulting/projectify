<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { Workspace } from "$lib/types/workspace";
    import Button from "$lib/figma/buttons/Button.svelte";
    import InputField from "$lib/figma/InputField.svelte";

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
        on:click={() => {
            console.error("Cancel not implemented");
        }}
        style={{ kind: "secondary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("edit-workspace-board.cancel")}
    />
    <Button
        on:click={() => {
            console.error("Save not implemented");
        }}
        style={{ kind: "primary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("invite-member.invite")}
    />
</div>
