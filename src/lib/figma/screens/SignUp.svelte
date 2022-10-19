<script lang="ts">
    import { _ } from "svelte-i18n";
    import { signUp } from "$lib/stores/user";
    import AuthScreen from "$lib/figma/screens/AuthScreen.svelte";
    import InputField from "$lib/figma/input-fields/InputField.svelte";
    import Button from "$lib/figma/buttons/Button.svelte";
    import Anchor from "$lib/figma/typography/Anchor.svelte";
    import CheckBox from "$lib/figma/select-controls/CheckBox.svelte";

    let email: string;
    let password: string;
    let tosPrivacyChecked: boolean;

    async function submit() {
        await signUp(email, password);
    }
</script>

<AuthScreen title={$_("sign-up.title")} action={submit}>
    <InputField
        placeholder={$_("sign-up.enter-your-email")}
        style={{ kind: "field", inputType: "text" }}
        name="email"
        label={$_("sign-up.email")}
        bind:value={email}
    />
    <InputField
        placeholder={$_("sign-up.enter-your-password")}
        style={{ kind: "field", inputType: "password" }}
        name="password"
        label={$_("sign-up.password")}
        bind:value={password}
    />
    <div class="TODO flex flex-row">
        <CheckBox
            bind:checked={tosPrivacyChecked}
            disabled={false}
            contained={false}
        />
        {$_("sign-up.i-agree")}
    </div>
    <Button
        on:click={submit}
        style={{ kind: "primary" }}
        color="blue"
        disabled={false}
        size="medium"
        label={$_("sign-up.sign-up")}
    />
    <div class="TODO">
        {$_("sign-up.already-have-an-account")}
        <Anchor
            href="/signin"
            label={$_("sign-up.log-in-here")}
            size="normal"
        />
    </div>
</AuthScreen>
