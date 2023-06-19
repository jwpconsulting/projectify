<script lang="ts">
    import { _ } from "svelte-i18n";
    import { signUp } from "$lib/stores/user";
    import AuthScreen from "$lib/figma/screens/auth/AuthScreen.svelte";
    import InputField from "$lib/figma/input-fields/InputField.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import Checkbox from "$lib/funabashi/select-controls/Checkbox.svelte";

    let email: string;
    let password: string;
    let tosPrivacyChecked: boolean;
    let error: string | undefined = undefined;

    async function action() {
        // TODO form validation
        error = undefined;
        try {
            await signUp(email, password);
        } catch {
            error = $_("sign-up.invalid-credentials");
        }
    }
</script>

<AuthScreen title={$_("sign-up.title")} {action}>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_("sign-up.enter-your-email")}
            style={{ kind: "field", inputType: "text" }}
            name="email"
            label={$_("sign-up.email")}
            bind:value={email}
            required
        />
        <InputField
            placeholder={$_("sign-up.enter-your-password")}
            style={{ kind: "field", inputType: "password" }}
            name="password"
            label={$_("sign-up.password")}
            bind:value={password}
            required
        />
        <div class="flex flex-row items-center gap-2">
            <Checkbox
                bind:checked={tosPrivacyChecked}
                disabled={false}
                contained={false}
            />
            <p>
                {$_("sign-up.i-agree")}
                <Anchor
                    href="/tos"
                    label={$_("sign-up.terms")}
                    size="normal"
                />
                {$_("sign-up.and")}
                <Anchor
                    href="/privacy"
                    label={$_("sign-up.privacy-statement")}
                    size="normal"
                />
            </p>
        </div>
        {#if error}
            <div>
                {error}
            </div>
        {/if}
        <Button
            action={{ kind: "button", action }}
            style={{ kind: "primary" }}
            color="blue"
            disabled={false}
            size="medium"
            label={$_("sign-up.sign-up")}
        />
        <div class="text-center">
            {$_("sign-up.already-have-an-account")}
            <Anchor
                href="/login"
                label={$_("sign-up.log-in-here")}
                size="normal"
            />
        </div>
    </div>
</AuthScreen>
