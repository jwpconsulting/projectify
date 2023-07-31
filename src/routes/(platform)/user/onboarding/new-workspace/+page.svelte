<script lang="ts">
    import { _ } from "svelte-i18n";

    import Onboarding from "$lib/components/Onboarding.svelte";
    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import type { PageData } from "./$types";
    import { createWorkspace } from "$lib/repository/workspace";
    import { goto } from "$lib/navigation";

    export let data: PageData;
    let { user } = data;

    let workspaceTitle: string | undefined = undefined;
    let state: OnboardingState = "new-workspace";

    $: workspaceTitleGiven = workspaceTitle && workspaceTitle.length > 0;

    async function nextAction() {
        if (!workspaceTitle) {
            throw new Error("Exepcted workspaceTitle");
        }
        await createWorkspace(workspaceTitle, "empty description TODO");
        await goto("/user/onboarding/new-board");
    }
</script>

<Onboarding
    title={$_("onboarding.new-workspace.title", {
        values: { who: user.full_name },
    })}
    prompt={$_("onboarding.new-workspace.prompt")}
    {nextAction}
    nextBtnDisabled={!workspaceTitleGiven}
    hasContentPadding={false}
>
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
