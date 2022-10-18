<script lang="ts">
    import { _ } from "svelte-i18n";
    import type { Workspace } from "$lib/types/workspace";
    import Button from "$lib/figma/buttons/Button.svelte";

    export let workspace: Workspace;
    console.log("TODO do something with", workspace);
</script>

<p class="text-center text-error">
    {$_("invite-member-error.notice")}
</p>
<div class="flex flex-row justify-center">
    <Button
        on:click={() => {
            console.error("Cancel not implemented");
        }}
        style={{ kind: "secondary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("invite-member-error.cancel")}
    />
    <Button
        on:click={() => {
            console.error("Save not implemented");
        }}
        style={{ kind: "primary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("invite-member-error.go-to-billing")}
    />
</div>
