<script lang="ts">
    import { _ } from "svelte-i18n";

    import { goto } from "$lib/navigation";
    import { getDashboardWorkspaceBoardUrl } from "$lib/urls";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { createWorkspaceBoard } from "$lib/repository/workspace";
    import {
        rejectConstructiveOverlay,
        resolveConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { Workspace } from "$lib/types/workspace";

    export let workspace: Workspace;

    let title: string | undefined = undefined;

    async function save() {
        if (!title) {
            throw new Error("Not valid");
        }
        const { uuid } = await createWorkspaceBoard(workspace, {
            title,
            description: "TODO",
            deadline: null,
        });
        await goto(getDashboardWorkspaceBoardUrl(uuid));
        resolveConstructiveOverlay();
    }
</script>

<form class="flex flex-col gap-8" on:submit|preventDefault={save}>
    <input type="submit" class="hidden" />
    <div class="flex flex-col gap-2">
        <InputField
            name="workspace-board-name"
            label={$_(
                "overlay.constructive.create-workspace-board.form.title.label"
            )}
            placeholder={$_(
                "overlay.constructive.create-workspace-board.form.title.placeholder"
            )}
            style={{ kind: "field", inputType: "text" }}
            bind:value={title}
        />
        <InputField
            name="deadline"
            label={$_(
                "overlay.constructive.create-workspace-board.form.deadline.label"
            )}
            placeholder={$_(
                "overlay.constructive.create-workspace-board.form.deadline.placeholder"
            )}
            style={{ kind: "field", inputType: "text" }}
        />
    </div>
    <div class="flex flex-row justify-center">
        <Button
            action={{
                kind: "button",
                action: rejectConstructiveOverlay,
            }}
            style={{ kind: "secondary" }}
            size="medium"
            color="blue"
            label={$_("overlay.constructive.create-workspace-board.cancel")}
        />
        <Button
            action={{ kind: "submit" }}
            style={{ kind: "primary" }}
            size="medium"
            color="blue"
            label={$_(
                "overlay.constructive.create-workspace-board.create-board"
            )}
        />
    </div>
</form>
