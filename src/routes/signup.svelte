<script lang="ts">
    import { spring } from "svelte/motion";
    import delay from "delay";
    import { singUp } from "$lib/stores/user";
    import { goto } from "$app/navigation";
    import { _ } from "svelte-i18n";
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";

    let errorAnimation = spring(0, {
        stiffness: 0.3,
        damping: 0.2,
    });

    let emailValue;
    let passwordValue;

    let privacyChecked = false;

    let error = false;
    let userData = null;

    async function submit() {
        userData = await singUp(emailValue, passwordValue);

        if (!userData) {
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
        {#if !userData}
            <form
                class="contents"
                action="/signup"
                method="post"
                on:submit|preventDefault={() => submit()}
            >
                <div
                    class="card text-center shadow-card w-full max-w-xl transform-gpu"
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
                            class="p-2  hi form-pop-msg text-error"
                            class:hidden={!error}
                        >
                            {$_("user-already-exist")}
                        </div>
                        <div class="flex  py-4">
                            <input
                                type="checkbox"
                                name="privacy"
                                class="checkbox shrink-0"
                                bind:checked={privacyChecked}
                            />
                            <label
                                for="privacy"
                                class="text-xs ml-2 text-left"
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
                class="card text-center shadow-card w-full max-w-xl transform-gpu"
            >
                <div class="card-body items-center">
                    <div class="py-2">
                        <h1 class="card-title">{$_("email-sent")}</h1>
                        <div>
                            {$_("i-sent-an-email-to")}
                            <span class="link link-primary"
                                >{userData.email}</span
                            >. {$_(
                                "please-proceed-from-the-url-described-in-the-message"
                            )}<wbr />
                        </div>
                    </div>
                    <div class="pt-2">
                        <button class="btn btn-primary" on:click={gotoTopPage}>
                            {$_("top-page")}
                        </button>
                    </div>
                </div>
            </div>
        {/if}
    </main>
</PageLayout>
