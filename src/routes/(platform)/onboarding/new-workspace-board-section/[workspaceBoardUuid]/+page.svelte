<script lang="ts">
    import { _ } from "svelte-i18n";

    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";

    const workspaceTitle = "";
    const boardTitle = "";
    const taskTitle = "";
    const state: OnboardingState = "new-section";
</script>

<Onboarding
    title={$_("onboarding.new-section.title")}
    hasContentPadding={false}
    stepCount={5}
    step={3}
>
    <svelte:fragment slot="prompt">
        <p>Add new sections and customise your section names.</p>
    </svelte:fragment>

    <svelte:fragment slot="content">
        <AppIllustration {state} {workspaceTitle} {boardTitle} {taskTitle} />
    </svelte:fragment>
</Onboarding>
