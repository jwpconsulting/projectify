<script lang="ts">
    import Onboarding from "$lib/components/onboarding.svelte";
    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";

    let workspaceTitle = "";
    let state: OnboardingState = "new-workspace";
</script>

<Onboarding
    title={"Let’s set up your first workspace, full name."}
    prompt={"You can create and manage numerous workspaces"}
    nextBtnDisabled={!workspaceTitle}
    hasContentPadding={false}
>
    <svelte:fragment slot="inputs">
        <input
            type="text"
            name="workspaceTitle"
            class="input input-bordered"
            placeholder="e.g. the name of your company"
            bind:value={workspaceTitle}
        />
    </svelte:fragment>

    <svelte:fragment slot="content">
        <AppIllustration {state} {workspaceTitle} />
    </svelte:fragment>
</Onboarding>
