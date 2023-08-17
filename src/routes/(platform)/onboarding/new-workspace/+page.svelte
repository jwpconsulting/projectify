<script lang="ts">
    import { _ } from "svelte-i18n";

    import { goto } from "$lib/navigation";

    import type { PageData } from "./$types";

    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { createWorkspace } from "$lib/repository/workspace";
    import type { OnboardingState } from "$lib/types/onboarding";
    import { getNewWorkspaceBoardUrl } from "$lib/urls/onboarding";

    export let data: PageData;
    let { user, workspace } = data;

    let workspaceTitle: string | undefined = undefined;
    let state: OnboardingState = "new-workspace";

    $: workspaceTitleGiven = workspaceTitle && workspaceTitle.length > 0;

    async function action() {
        if (!workspaceTitle) {
            throw new Error("Exepcted workspaceTitle");
        }
        const { uuid } = await createWorkspace(
            workspaceTitle,
            "empty description TODO"
        );

        const nextStep = getNewWorkspaceBoardUrl(uuid);
        await goto(nextStep);
    }
</script>

<Onboarding
    title={$_("onboarding.new-workspace.title", {
        values: { who: user.full_name },
    })}
    prompt={workspace ? null : $_("onboarding.new-workspace.prompt")}
    nextAction={{ kind: "button", action }}
    nextBtnDisabled={!workspaceTitleGiven}
    hasContentPadding={false}
>
    <svelte:fragment slot="prompt">
        {#if workspace}
            <p>
                {$_("onboarding.new-workspace.has-workspace")}
            </p>
            <p>
                <Anchor
                    size="large"
                    href={getNewWorkspaceBoardUrl(workspace.uuid)}
                    label={"Create workspace board"}
                />
            </p>
        {/if}
    </svelte:fragment>
    <svelte:fragment slot="inputs">
        <InputField
            style={{ kind: "field", inputType: "text" }}
            name="workspaceTitle"
            placeholder={$_("onboarding.new-workspace.placeholder")}
            bind:value={workspaceTitle}
        />
    </svelte:fragment>

    <svelte:fragment slot="content">
        <AppIllustration {state} {workspaceTitle} />
    </svelte:fragment>
</Onboarding>
