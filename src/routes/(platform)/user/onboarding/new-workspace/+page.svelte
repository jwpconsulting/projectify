<script lang="ts">
    import { _ } from "svelte-i18n";

    import Onboarding from "$lib/components/Onboarding.svelte";
    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    let workspaceTitle: string | undefined = undefined;
    let state: OnboardingState = "new-workspace";

    $: workspaceTitleGiven = workspaceTitle && workspaceTitle.length > 0;

    async function nextAction() {}
</script>

<Onboarding
    title={$_("onboarding.new-workspace.title")}
    prompt={$_("onboarding.new-workspace.prompt")}
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
