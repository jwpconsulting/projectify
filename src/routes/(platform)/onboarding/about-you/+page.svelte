<script lang="ts">
    import { _ } from "svelte-i18n";

    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { goto } from "$lib/navigation";
    import { updateUserProfile } from "$lib/stores/user";
    import { newWorkspaceUrl } from "$lib/urls/onboarding";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { user } = data;

    let fullName: string | undefined = user.full_name;

    $: disabled = fullName === undefined;

    async function submit() {
        if (fullName == undefined) {
            throw new Error("Expected fullName");
        }
        await updateUserProfile(fullName);
        await goto(newWorkspaceUrl);
    }
</script>

<Onboarding
    title={$_("onboarding.about-you.title")}
    prompt={$_("onboarding.about-you.prompt")}
    hasContentPadding={true}
    nextAction={{ kind: "submit", disabled, submit }}
>
    <svelte:fragment slot="inputs">
        <InputField
            bind:value={fullName}
            placeholder={$_("onboarding.about-you.full-name")}
            style={{ kind: "field", inputType: "text" }}
            name="full-name"
            required
        />
    </svelte:fragment>

    <svelte:fragment slot="content-title">
        Welcome{#if !disabled},
        {/if}{fullName ?? ""}! 👋
    </svelte:fragment>

    <svelte:fragment slot="content">
        <div>User Profile picture</div>
    </svelte:fragment>
</Onboarding>
