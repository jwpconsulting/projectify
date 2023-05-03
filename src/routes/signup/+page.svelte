<script lang="ts">
    import { spring } from "svelte/motion";
    import delay from "delay";
    import { _ } from "svelte-i18n";
    import { signUp } from "$lib/stores/user";
    import { goto } from "$app/navigation";
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import IllustrationEmailSent from "$lib/components/illustrations/illustration-email-sent.svelte";

    let errorAnimation = spring(0, {
        stiffness: 0.3,
        damping: 0.2,
    });

    let emailValue: string;
    let passwordValue: string;

    let privacyChecked = false;

    let error = false;
    let submittedEmail: string | null = null;

    async function submit() {
        submittedEmail = await signUp(emailValue, passwordValue);

        if (!submittedEmail) {
            error = true;
            errorAnimation.set(-50);
            await delay(100);
            errorAnimation.set(0);
        }
    }

    function unsetError() {
        error = false;
    }

    function gotoTopPage() {
        goto("/");
    }
</script>

<PageLayout>
    <main class="page page-center bg-base-200">
        {#if !submittedEmail}
            <form
                class="contents"
                action="/signup"
                method="post"
                on:submit|preventDefault={() => submit()}
            >
                <div
                    class="card w-full max-w-xl transform-gpu text-center shadow-card"
                    style={`transform:translateX(${$errorAnimation}px);`}
                >
                    <div class="card-body items-center">
                        <div class="py-2">
                            <h1 class="card-title">
                                {$_("sign-up")}
                            </h1>
                            <div>
                                {$_("page.signup.msg")}<wbr />
                                <a class="link link-primary" href="/signin">
                                    {$_("sign-in-here")}
                                </a>
                            </div>
                        </div>

                        <div class="form-control w-full">
                            <label for="email" class="label label-text"
                                >{$_("email")}</label
                            >
                            <input
                                type="email"
                                id="email"
                                name="email"
                                autocomplete="email"
                                placeholder={$_("please-enter-your-email")}
                                class="input input-bordered"
                                class:input-error={error}
                                bind:value={emailValue}
                                on:input={unsetError}
                            />
                        </div>

                        <div class="form-control w-full">
                            <label for="password" class="label label-text"
                                >{$_("password")}</label
                            >
                            <input
                                type="password"
                                id="password"
                                name="password"
                                autocomplete="new-password"
                                placeholder={$_("please-enter-a-password")}
                                class="input input-bordered"
                                class:input-error={error}
                                bind:value={passwordValue}
                                on:input={unsetError}
                            />
                        </div>
                        <div
                            class="hi form-pop-msg p-2 text-error"
                            class:hidden={!error}
                        >
                            {$_("user-already-exist")}
                        </div>
                        <div class="flex py-4">
                            <input
                                type="checkbox"
                                name="privacy"
                                class="checkbox shrink-0"
                                bind:checked={privacyChecked}
                            />
                            <label
                                for="privacy"
                                class="ml-2 text-left text-xs"
                            >
                                {$_("signup-privacy")}
                            </label>
                        </div>
                        <div class="pt-2">
                            <button
                                class="btn btn-primary rounded-full"
                                type="submit"
                                disabled={!privacyChecked}
                            >
                                {$_("sign-up")}
                            </button>
                        </div>
                    </div>
                </div>
            </form>
        {:else}
            <div
                class="card w-full max-w-xl transform-gpu text-center shadow-card"
            >
                <div class="card-body items-center">
                    <div class="py-2">
                        <div class="flex items-center justify-center pb-2">
                            <IllustrationEmailSent />
                        </div>
                        <h1 class="card-title">{$_("email-sent")}</h1>
                        <div>
                            {$_("i-sent-an-email-to")}
                            <span class="link link-primary"
                                >{submittedEmail}</span
                            >. {$_(
                                "please-proceed-from-the-url-described-in-the-message"
                            )}<wbr />
                        </div>
                    </div>
                    <div class="pt-2">
                        <button class="btn-action btn" on:click={gotoTopPage}>
                            {$_("top-page")}
                        </button>
                    </div>
                </div>
            </div>
        {/if}
    </main>
</PageLayout>
