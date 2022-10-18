<script lang="ts">
    import { _ } from "svelte-i18n";
    import Button from "$lib/figma/buttons/Button.svelte";
</script>

<p class="text-center">
    {$_("new-workspace.notice")}
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
        label={$_("new-workspace.cancel")}
    />
    <Button
        on:click={() => {
            console.error("Save not implemented");
        }}
        style={{ kind: "primary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("new-workspace.create-workspace")}
    />
</div>
