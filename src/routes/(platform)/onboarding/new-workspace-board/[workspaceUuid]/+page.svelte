<script lang="ts">
    import { _, json } from "svelte-i18n";

    import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import { createWorkspaceBoard } from "$lib/repository/workspace/workspaceBoard";
    import { getNewTaskUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { workspace, workspaceBoard } = data;

    let title: string | undefined = undefined;

    $: disabled = title === undefined;

    async function submit() {
        if (!title) {
            throw new Error("Expected title");
        }
        const { uuid } = await createWorkspaceBoard(
            workspace,
            {
                title,
                description: "",
            },
            { fetch }
        );
        const nextStep = getNewTaskUrl(uuid);
        await goto(nextStep);
    }

    $: prompts = $json("onboarding.new-workspace-board.prompt") as string[];
</script>

<Onboarding
    hasContentPadding={false}
    stepCount={5}
    step={1}
    nextAction={{
        kind: "submit",
        disabled,
        submit,
    }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.new-workspace-board.title")}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        <div class="flex flex-col gap-8">
            {#if workspaceBoard}
                <div class="flex flex-col gap-4">
                    <p>
                        {$_(
                            "onboarding.new-workspace-board.workspace-board-exists.message",
                            { values: { title: workspaceBoard.title } }
                        )}
                    </p>
                    <p>
                        <Anchor
                            label={$_(
                                "onboarding.new-workspace-board.workspace-board-exists.prompt",
                                { values: { title: workspaceBoard.title } }
                            )}
                            size="large"
                            href={getNewTaskUrl(workspaceBoard.uuid)}
                        />
                    </p>
                </div>
            {:else}
                <div class="flex flex-col gap-3">
                    {#each prompts as prompt}
                        <p>{prompt}</p>
                    {/each}
                </div>
            {/if}
        </div>
    </svelte:fragment>

    <svelte:fragment slot="inputs">
        <InputField
            style={{ kind: "field", inputType: "text" }}
            name="title"
            label={$_("onboarding.new-workspace-board.input.label")}
            placeholder={$_(
                "onboarding.new-workspace-board.input.placeholder"
            )}
            bind:value={title}
            required
        />
    </svelte:fragment>

    <DashboardPlaceholder
        slot="content"
        state={{
            kind: "new-workspace-board",
            workspace,
            workspaceBoard,
            title:
                title ??
                workspaceBoard?.title ??
                $_("onboarding.new-workspace-board.default-name"),
        }}
    />
</Onboarding>
