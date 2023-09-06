<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/figma/overlays/constructive/Layout.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { rejectConstructiveOverlay } from "$lib/stores/globalUi";
</script>

<Layout>
    <svelte:fragment slot="title">
        {$_("overlay.constructive.create-workspace.title")}
    </svelte:fragment>
    <svelte:fragment slot="form">
        <p class="text-center">
            {$_("overlay.constructive.create-workspace.notice")}
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
                label={$_("overlay.constructive.create-workspace.cancel")}
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
                label={$_(
                    "overlay.constructive.create-workspace.create-workspace"
                )}
            />
        </div>
    </svelte:fragment>
</Layout>
