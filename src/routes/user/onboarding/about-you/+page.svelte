<script lang="ts">
    import { _ } from "svelte-i18n";
    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    let fullName = "";
</script>

<Onboarding
    title={$_("onboarding.about-you.title")}
    prompt={$_("onboarding.about-you.prompt")}
    nextBtnDisabled={!fullName}
    hasContentPadding={true}
>
    <svelte:fragment slot="inputs">
        <InputField
            bind:value={fullName}
            placeholder={$_("onboarding.about-you.full-name")}
            style={{ kind: "field", inputType: "text" }}
            name="full-name"
        />
    </svelte:fragment>

    <svelte:fragment slot="content-title">
        Welcome{#if fullName},{/if}
        {fullName}! 👋
    </svelte:fragment>

    <svelte:fragment slot="content">
        <div>User Profile picture</div>
    </svelte:fragment>
</Onboarding>
