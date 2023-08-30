<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { rejectConstructiveOverlay } from "$lib/stores/globalUi";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;
    console.log("TODO do something with", workspace);
</script>

<p class="text-center text-error">
    {$_("invite-member-error.notice")}
</p>
<div class="flex flex-row justify-center">
    <Button
        action={{
            kind: "button",
            action: rejectConstructiveOverlay,
        }}
        style={{ kind: "secondary" }}
        size="medium"
        color="blue"
        label={$_("invite-member-error.cancel")}
    />
    <Button
        action={{
            kind: "button",
            action: () => {
                console.error("Save not implemented");
            },
        }}
        style={{ kind: "primary" }}
        size="medium"
        color="blue"
        label={$_("invite-member-error.go-to-billing")}
    />
</div>
