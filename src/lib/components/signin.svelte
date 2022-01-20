<script lang="ts">
    import { spring } from "svelte/motion";
    import delay from "delay";
    import { login } from "$lib/stores/user";

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
    class="card text-center shadow-card w-full max-w-xl transform-gpu"
    style={`transform:translateX(${$errorAnimation}px);`}
>
    <form on:submit|preventDefault={() => submit()}>
        <div class="card-body items-center">
            <div class="py-2">
                <h1 class="card-title">Sign in</h1>
                <div>
                    Let’s set up your account, Don't have one yet?<wbr />
                    <a class="link link-primary" href="/signup">
                        Sign up here.
                    </a>
                </div>
            </div>

            <div class="form-control w-full">
                <label for="email" class="label label-text">Email</label>
                <input
                    type="text"
                    name="email"
                    placeholder="Please enter your email"
                    class="input input-bordered"
                    class:input-error={error}
                    bind:value={emailValue}
                    on:input={unsetError}
                />
            </div>

            <div class="form-control w-full">
                <label for="password" class="label label-text">Password</label>
                <input
                    type="password"
                    name="password"
                    placeholder="Please enter a password"
                    class="input input-bordered"
                    class:input-error={error}
                    bind:value={passwordValue}
                    on:input={unsetError}
                />
            </div>
            <div class="p-2  hi form-pop-msg text-error" class:hidden={!error}>
                Wrong email or password.
            </div>

            <div class="pt-7">
                <button class="btn btn-primary rounded-full" type="submit">
                    Sign in
                </button>
                <div class="p-2">
                    Forget password? Password reset
                    <a class="link link-primary" href="/user/reset">here.</a>
                </div>
            </div>
        </div>
    </form>
</div>
