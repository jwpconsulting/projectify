<script lang="ts">
    import { spring } from "svelte/motion";
    import delay from "delay";
    import { login } from "$lib/stores/user";
    import { _ } from "svelte-i18n";

    let errorAnimation = spring(0, {
        stiffness: 0.3,
        damping: 0.2,
    });

    let emailValue;
    let passwordValue;

    let error = false;

    async function submit() {
        const userData = await login(emailValue, passwordValue);

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
</script>

<div
    class="card w-full max-w-xl transform-gpu text-center shadow-card"
    style={`transform:translateX(${$errorAnimation}px);`}
>
    <form
        class="contents"
        action="/signin"
        method="post"
        on:submit|preventDefault={() => submit()}
    >
        <div class="card-body items-center">
            <div class="py-2">
                <h1 class="card-title">{$_("sign-in")}</h1>
                <div>
                    {$_("lets-set-up-your-account-dont-have-one-yet")}<wbr />
                    <a class="link link-primary" href="/signup">
                        {$_("sign-up-here")}
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
                    autocomplete="current-password"
                    placeholder={$_("please-enter-a-password")}
                    class="input input-bordered"
                    class:input-error={error}
                    bind:value={passwordValue}
                    on:input={unsetError}
                />
            </div>
            <div class="hi  form-pop-msg p-2 text-error" class:hidden={!error}>
                {$_("wrong-email-or-password")}
            </div>

            <div class="pt-7">
                <button class="btn btn-primary rounded-full" type="submit">
                    {$_("sign-in")}
                </button>
                <div class="p-2">
                    {$_("forget-password-password-reset")}
                    <a class="link link-primary" href="/user/reset"
                        >{$_("here")}</a
                    >
                </div>
            </div>
        </div>
    </form>
</div>
