<script lang="ts">
    import { _ } from "svelte-i18n";
    import Button from "$lib/funabashi/buttons/Button.svelte";
</script>

<p class="text-center text-error">
    {$_("skip-onboarding.notice")}
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
        disabled={false}
        color="blue"
        label={$_("skip-onboarding.cancel")}
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
        disabled={false}
        color="blue"
        label={$_("skip-onboarding.skip-onboarding")}
    />
</div>
