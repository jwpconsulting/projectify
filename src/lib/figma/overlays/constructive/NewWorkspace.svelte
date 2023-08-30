<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
</script>

<p class="text-center">
    {$_("new-workspace.notice")}
</p>
<div class="flex flex-row justify-center">
    <Button
        action={{
            kind: "button",
            action: () => {
                console.error("Cancel not implemented");
            },
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
