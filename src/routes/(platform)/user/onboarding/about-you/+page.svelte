<script lang="ts">
    import { _ } from "svelte-i18n";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { updateUserProfile } from "$lib/stores/user";
    import { goto } from "$lib/navigation";

    let fullName: string | undefined = undefined;

    $: nextBtnDisabled = fullName === undefined || fullName.length == 0;

    async function nextAction() {
        if (fullName == undefined) {
            throw new Error("Expected fullName");
        }
        await updateUserProfile(fullName);
        await goto("/user/onboarding/new-workspace");
    }
</script>

<Onboarding
    title={$_("onboarding.about-you.title")}
    prompt={$_("onboarding.about-you.prompt")}
    {nextBtnDisabled}
    hasContentPadding={true}
    {nextAction}
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
        Welcome{#if !nextBtnDisabled}, {/if}{fullName ?? ""}! 👋
    </svelte:fragment>

    <svelte:fragment slot="content">
        <div>User Profile picture</div>
    </svelte:fragment>
</Onboarding>
