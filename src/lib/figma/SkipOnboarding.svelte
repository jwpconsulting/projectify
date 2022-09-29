<script lang="ts">
    import { _ } from "svelte-i18n";
    import Button from "$lib/figma/Button.svelte";
</script>

<p class="text-center text-error">
    {$_("skip-onboarding.notice")}
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
        label={$_("skip-onboarding.cancel")}
    />
    <Button
        on:click={() => {
            console.error("Save not implemented");
        }}
        style={{ kind: "primary" }}
        size="medium"
        disabled={false}
        color="blue"
        label={$_("skip-onboarding.skip-onboarding")}
    />
</div>
