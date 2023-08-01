<script lang="ts">
    import { _ } from "svelte-i18n";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { PageData } from "./$types";
    import {
        createWorkspaceBoard,
        createWorkspaceBoardSection,
    } from "$lib/repository/workspace";
    import { goto } from "$app/navigation";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { getDashboardWorkspaceBoardUrl, getNewTaskUrl } from "$lib/urls";

    export let data: PageData;

    const { workspace, workspaceBoard, workspaceBoardSection } = data;

    let title: string | undefined = workspaceBoard?.title;
    let state: OnboardingState = "new-board";

    async function nextAction() {
        if (!title) {
            throw new Error("Expected title");
        }
        const workspaceBoard = await createWorkspaceBoard(workspace, {
            title,
            description: "",
            // TODO please make me optional
            deadline: null,
        });
        const { uuid } = await createWorkspaceBoardSection(workspaceBoard, {
            title: "To Do",
            description: "",
        });
        const nextStep = getNewTaskUrl(uuid);
        await goto(nextStep);
    }
</script>

<Onboarding
    title={$_("onboarding.new-workspace-board.title")}
    hasContentPadding={false}
    stepCount={5}
    step={1}
    {nextAction}
>
    <svelte:fragment slot="prompt">
        <div class="flex flex-col gap-8">
            {#if workspaceBoard && workspaceBoardSection}
                <div class="flex flex-col gap-4">
                    <p>
                        {$_(
                            "onboarding.new-workspace-board.workspace-board-section-exists.message",
                            {
                                values: {
                                    title: workspaceBoard.title,
                                    section: workspaceBoardSection.title,
                                },
                            }
                        )}
                    </p>
                    <p>
                        <Anchor
                            label={$_(
                                "onboarding.new-workspace-board.workspace-board-section-exists.prompt"
                            )}
                            size="large"
                            href={getNewTaskUrl(workspaceBoardSection.uuid)}
                        />
                    </p>
                </div>
            {:else if workspaceBoard}
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
                                "onboarding.new-workspace-board.workspace-board-exists.prompt"
                            )}
                            size="large"
                            href={getDashboardWorkspaceBoardUrl(
                                workspaceBoard.uuid
                            )}
                        />
                    </p>
                </div>
            {:else}
                <div>
                    {#each $_("onboarding.new-workspace-board.prompt") as prompt}
                        <p>{prompt}</p>
                    {/each}
                </div>
            {/if}
        </div></svelte:fragment
    >

    <svelte:fragment slot="inputs">
        <InputField
            style={{ kind: "field", inputType: "text" }}
            name="title"
            label={$_("onboarding.new-workspace-board.input.label")}
            placeholder={$_(
                "onboarding.new-workspace-board.input.placeholder"
            )}
            bind:value={title}
        />
    </svelte:fragment>

    <svelte:fragment slot="content">
        <AppIllustration
            {state}
            workspaceTitle={workspace.title}
            boardTitle={title ??
                $_("onboarding.new-workspace-board.default-name")}
        />
    </svelte:fragment>
</Onboarding>
