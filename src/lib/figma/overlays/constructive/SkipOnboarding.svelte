<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/figma/overlays/constructive/Layout.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { rejectConstructiveOverlay } from "$lib/stores/globalUi";
</script>

<Layout>
    <svelte:fragment slot="title">
        {$_("overlay.constructive.skip-onboarding.title")}
    </svelte:fragment>
    <svelte:fragment slot="message">
        <p class="text-center text-error">
            {$_("overlay.constructive.skip-onboarding.notice")}
        </p>
    </svelte:fragment>
    <svelte:fragment slot="buttons">
        <Button
            action={{
                kind: "button",
                action: rejectConstructiveOverlay,
            }}
            style={{ kind: "secondary" }}
            size="medium"
            color="blue"
            label={$_("overlay.constructive.skip-onboarding.cancel")}
        />
        <Button
            action={{
                kind: "a",
                href: "/",
            }}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
            label={$_("overlay.constructive.skip-onboarding.skip-onboarding")}
        />
    </svelte:fragment>
</Layout>
