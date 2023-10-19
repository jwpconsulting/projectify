<script lang="ts">
    import { _ } from "svelte-i18n";

    import AuthScreen from "$lib/figma/screens/auth/AuthScreen.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Checkbox from "$lib/funabashi/select-controls/Checkbox.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import { signUp } from "$lib/stores/user";

    let email: string;
    let password: string;
    let tosPrivacyChecked: boolean;
    let error: string | undefined = undefined;

    async function action() {
        // TODO form validation
        error = undefined;
        try {
            await signUp(email, password);
            await goto("/email-confirmation-link-sent/");
        } catch {
            error = $_("auth.sign-up.invalid-credentials");
        }
    }
</script>

<AuthScreen
    title={$_("auth.sign-up.title")}
    {action}
    subTitle={$_("auth.sign-up.sub-title")}
>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_("auth.sign-up.enter-your-email")}
            style={{ kind: "field", inputType: "text" }}
            name="email"
            label={$_("auth.sign-up.email")}
            bind:value={email}
            required
        />
        <InputField
            placeholder={$_("auth.sign-up.enter-your-password")}
            style={{ kind: "field", inputType: "password" }}
            name="password"
            label={$_("auth.sign-up.password")}
            bind:value={password}
            required
        />
        <div class="flex flex-row items-center gap-2">
            <Checkbox
                bind:checked={tosPrivacyChecked}
                disabled={false}
                contained={false}
                required
            />
            <p>
                {$_("auth.sign-up.tos-privacy.i-agree")}
                <Anchor
                    href="/tos"
                    label={$_("auth.sign-up.tos-privacy.terms")}
                    size="normal"
                />
                {$_("auth.sign-up.tos-privacy.and")}
                <Anchor
                    href="/privacy"
                    label={$_("auth.sign-up.tos-privacy.privacy-statement")}
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
            action={{ kind: "submit" }}
            style={{ kind: "primary" }}
            color="blue"
            size="medium"
            label={$_("auth.sign-up.sign-up")}
        />
        <div class="text-center">
            {$_("auth.sign-up.already-have-an-account")}
            <Anchor
                href="/login"
                label={$_("auth.sign-up.log-in-here")}
                size="normal"
            />
        </div>
    </div>
</AuthScreen>
