<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/figma/overlays/constructive/Layout.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { rejectConstructiveOverlay } from "$lib/stores/globalUi";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;
    console.log("TODO do something with", workspace);
</script>

<Layout>
    <svelte:fragment slot="title">
        {$_("overlay.constructive.invite-member-error.title")}
    </svelte:fragment>
    <svelte:fragment slot="form">
        <p class="text-center text-error">
            {$_("overlay.constructive.invite-member-error.notice")}
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
                label={$_("overlay.constructive.invite-member-error.cancel")}
            />
            <Button
                action={{
                    kind: "a",
                    href: "/",
                }}
                style={{ kind: "primary" }}
                size="medium"
                color="blue"
                label={$_(
                    "overlay.constructive.invite-member-error.go-to-billing"
                )}
            />
        </div>
    </svelte:fragment>
</Layout>
