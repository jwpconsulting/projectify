<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { rejectConstructiveOverlay } from "$lib/stores/globalUi";
</script>

<p class="text-center text-error">
    {$_("skip-onboarding.notice")}
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
        color="blue"
        label={$_("skip-onboarding.skip-onboarding")}
    />
</div>
