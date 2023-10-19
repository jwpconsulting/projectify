<script lang="ts">
    import { _ } from "svelte-i18n";

    import AppIllustration from "$lib/components/onboarding/app-illustration.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import { createWorkspace } from "$lib/repository/workspace";
    import type { OnboardingState } from "$lib/types/onboarding";
    import { getNewWorkspaceBoardUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";

    export let data: PageData;
    const { user, workspace } = data;

    let workspaceTitle: string | undefined = undefined;
    const state: OnboardingState = "new-workspace";

    $: disabled = workspaceTitle === undefined;

    async function submit() {
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
    nextAction={{ kind: "submit", disabled, submit }}
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
