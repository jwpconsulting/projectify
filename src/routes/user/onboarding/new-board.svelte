<script lang="ts">
    import Onboarding from "$lib/components/onboarding.svelte";
    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import type { OnboardingState } from "$lib/types/onboarding";

    let workspaceTitle = "";
    let boardTitle = "";
    let state: OnboardingState = "new-board";
</script>

<Onboarding
    title={"Add your first board"}
    hasContentPadding={false}
    stepCount={5}
    step={1}
>
    <svelte:fragment slot="prompt">
        <p>
            You can create unlimited boards per workspace.
            <br />They help you to focus on different projects you may be
            working on.
        </p>
    </svelte:fragment>

    <svelte:fragment slot="inputs">
        <input
            type="text"
            name="boardTitle"
            class="input input-bordered"
            placeholder="e.g. marketing for Q1"
            bind:value={boardTitle}
        />
    </svelte:fragment>

    <svelte:fragment slot="content">
        <AppIllustration {state} {workspaceTitle} {boardTitle} />
    </svelte:fragment>
</Onboarding>
