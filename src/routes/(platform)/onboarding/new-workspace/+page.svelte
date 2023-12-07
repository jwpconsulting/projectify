<script lang="ts">
    import { _ } from "svelte-i18n";

    import DashboardPlaceholder from "$lib/components/onboarding/DashboardPlaceholder.svelte";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import { createWorkspace } from "$lib/repository/workspace";
    import { user } from "$lib/stores/user";
    import { getNewWorkspaceBoardUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";

    export let data: PageData;
    const { workspace } = data;

    let workspaceTitle: string | undefined = undefined;

    $: disabled = workspaceTitle === undefined;

    $: who = $user?.full_name ?? data.user.full_name;

    async function submit() {
        if (!workspaceTitle) {
            throw new Error("Exepcted workspaceTitle");
        }
        const { uuid } = await createWorkspace(workspaceTitle, undefined, {
            fetch,
        });

        const nextStep = getNewWorkspaceBoardUrl(uuid);
        await goto(nextStep);
    }
</script>

<Onboarding nextAction={{ kind: "submit", disabled, submit }}>
    <svelte:fragment slot="title"
        >{$_("onboarding.new-workspace.title", {
            values: { who },
        })}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        {#if workspace}
            <p>{$_("onboarding.new-workspace.has-workspace")}</p>
            <p>
                <Anchor
                    size="large"
                    href={getNewWorkspaceBoardUrl(workspace.uuid)}
                    label={"Create workspace board"}
                />
            </p>
        {:else}
            <p>{$_("onboarding.new-workspace.prompt")}</p>
        {/if}
    </svelte:fragment>
    <svelte:fragment slot="inputs">
        <InputField
            style={{ kind: "field", inputType: "text" }}
            name="workspaceTitle"
            label={$_("onboarding.new-workspace.label")}
            placeholder={$_("onboarding.new-workspace.placeholder")}
            bind:value={workspaceTitle}
            required
        />
    </svelte:fragment>
    <DashboardPlaceholder
        slot="content"
        state={{
            kind: "new-workspace",
            workspace,
            title:
                workspaceTitle ?? $_("onboarding.new-workspace.default-name"),
        }}
    />
</Onboarding>
