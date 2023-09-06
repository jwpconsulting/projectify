<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { rejectConstructiveOverlay } from "$lib/stores/globalUi";
</script>

<p class="text-center">
    {$_("new-workspace.notice")}
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
        label={$_("new-workspace.cancel")}
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
        label={$_("new-workspace.create-workspace")}
    />
</div>
