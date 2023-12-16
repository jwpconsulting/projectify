<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/figma/overlays/constructive/Layout.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import {
        rejectConstructiveOverlay,
        resolveConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { WorkspaceBoardSection } from "$lib/types/workspace";

    export let workspaceBoardSection: WorkspaceBoardSection;

    let { title } = workspaceBoardSection;

    async function onSubmit() {
        // NOOP
        await new Promise(console.log);
        resolveConstructiveOverlay();
    }
</script>

<Layout {onSubmit}>
    <svelte:fragment slot="title">
        {$_("overlay.constructive.update-workspace-board-section.title")}
    </svelte:fragment>
    <svelte:fragment slot="form">
        <InputField
            name="workspace-board-name"
            label={$_(
                "overlay.constructive.update-workspace-board-section.form.title.label"
            )}
            placeholder={$_(
                "overlay.constructive.update-workspace-board-section.form.title.placeholder"
            )}
            style={{ inputType: "text" }}
            bind:value={title}
        />
    </svelte:fragment>
    <svelte:fragment slot="buttons">
        <Button
            action={{ kind: "button", action: rejectConstructiveOverlay }}
            style={{ kind: "secondary" }}
            size="medium"
            color="blue"
            label={$_(
                "overlay.constructive.update-workspace-board-section.cancel"
            )}
        />
        <Button
            action={{ kind: "submit" }}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
            label={$_(
                "overlay.constructive.update-workspace-board-section.update"
            )}
        />
    </svelte:fragment>
</Layout>
