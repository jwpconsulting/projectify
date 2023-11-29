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
        await updateUserProfile(fullName, { fetch });
        await goto(newWorkspaceUrl);
    }
</script>

<Onboarding
    hasContentPadding={true}
    nextAction={{ kind: "submit", disabled, submit }}
>
    <svelte:fragment slot="title"
        >{$_("onboarding.about-you.title")}</svelte:fragment
    >
    <svelte:fragment slot="prompt">
        {$_("onboarding.about-you.prompt")}
    </svelte:fragment>
    <svelte:fragment slot="inputs">
        <InputField
            bind:value={fullName}
            placeholder={$_("onboarding.about-you.full-name")}
            style={{ kind: "field", inputType: "text" }}
            name="full-name"
            required
        />
    </svelte:fragment>

    <svelte:fragment slot="content">
        <h1 class="text-4xl font-bold">
            {#if fullName}
                {$_("onboarding.about-you.greeting.with-name", {
                    values: { name: fullName },
                })}
            {:else}
                {$_("onboarding.about-you.greeting.without-name")}
            {/if}
        </h1>
    </svelte:fragment>
</Onboarding>
