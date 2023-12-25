<script lang="ts">
    import { _ } from "svelte-i18n";

    import AuthScreen from "$lib/figma/screens/auth/AuthScreen.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Checkbox from "$lib/funabashi/select-controls/Checkbox.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { goto } from "$lib/navigation";
    import { signUp } from "$lib/repository/user";
    import { logInUrl, sentEmailConfirmationLinkUrl } from "$lib/urls/user";

    let email: string;
    let password: string;
    let tosAgreed: boolean;
    let privacyPolicyAgreed: boolean;
    let error: string | undefined = undefined;

    async function action() {
        // TODO form validation
        error = undefined;
        try {
            await signUp(email, password, tosAgreed, privacyPolicyAgreed, {
                fetch,
            });
            await goto(sentEmailConfirmationLinkUrl);
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
            style={{ inputType: "text" }}
            name="email"
            label={$_("auth.sign-up.email")}
            bind:value={email}
            required
        />
        <InputField
            placeholder={$_("auth.sign-up.enter-your-password")}
            style={{ inputType: "password" }}
            name="password"
            label={$_("auth.sign-up.password")}
            bind:value={password}
            required
        />
        <!-- XXX false positive -->
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label class="flex flex-row items-center gap-2">
            <Checkbox
                bind:checked={tosAgreed}
                disabled={false}
                contained={false}
                required
            />
            <span class="prose">
                <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                {@html $_("auth.sign-up.tos.label", {
                    values: {
                        tosUrl: "/tos",
                    },
                })}</span
            >
        </label>
        <!-- XXX false positive -->
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label class="flex flex-row items-center gap-2">
            <Checkbox
                bind:checked={privacyPolicyAgreed}
                disabled={false}
                contained={false}
                required
            />
            <span class="prose">
                <!-- eslint-disable-next-line svelte/no-at-html-tags -->
                {@html $_("auth.sign-up.privacy-policy.label", {
                    values: {
                        privacyPolicyUrl: "/privacy",
                    },
                })}</span
            >
        </label>
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
                href={logInUrl}
                label={$_("auth.sign-up.log-in-here")}
                size="normal"
            />
        </div>
    </div>
</AuthScreen>
