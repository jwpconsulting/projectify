<script lang="ts">
    import { _ } from "svelte-i18n";
    import { login } from "$lib/stores/user";
    import AuthScreen from "$lib/figma/screens/auth/AuthScreen.svelte";
    import InputField from "$lib/figma/input-fields/InputField.svelte";
    import Button from "$lib/figma/buttons/Button.svelte";
    import Anchor from "$lib/figma/typography/Anchor.svelte";

    let email: string;
    let password: string;

    async function submit() {
        // TODO validate form
        await login(email, password);
    }
</script>

<AuthScreen title={$_("log-in.title")} action={submit}>
    <div class="flex flex-col gap-6">
        <InputField
            placeholder={$_("log-in.enter-your-email")}
            style={{ kind: "field", inputType: "text" }}
            name="email"
            label={$_("log-in.email")}
            bind:value={email}
        />
        <InputField
            placeholder={$_("log-in.enter-your-password")}
            style={{ kind: "field", inputType: "password" }}
            name="password"
            label={$_("log-in.password")}
            bind:value={password}
            anchorBottom={{
                href: "/user/reset",
                label: $_("log-in.forgot-password"),
            }}
        />
        <Button
            on:click={submit}
            style={{ kind: "primary" }}
            color="blue"
            disabled={false}
            size="medium"
            label={$_("log-in.log-in")}
        />
        <div class="text-center">
            {$_("log-in.no-account")}
            <Anchor
                href="/signup"
                label={$_("log-in.sign-up-here")}
                size="normal"
            />
        </div>
    </div>
</AuthScreen>
