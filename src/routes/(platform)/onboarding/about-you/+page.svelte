<script lang="ts">
    import { _ } from "svelte-i18n";

    import { goto } from "$lib/navigation";

    import type { PageData } from "./$types";

    import Onboarding from "$lib/components/Onboarding.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import { updateUserProfile } from "$lib/stores/user";

    export let data: PageData;

    const { user } = data;

    let fullName: string | undefined = user.full_name;

    $: nextBtnDisabled = fullName === undefined || fullName.length == 0;

    async function action() {
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
    nextAction={{ kind: "button", action }}
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
        Welcome{#if !nextBtnDisabled},
        {/if}{fullName ?? ""}! 👋
    </svelte:fragment>

    <svelte:fragment slot="content">
        <div>User Profile picture</div>
    </svelte:fragment>
</Onboarding>
