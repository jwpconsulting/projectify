<script lang="ts">
    import { spring } from "svelte/motion";
    import delay from "delay";
    import { singUp } from "$lib/stores/user";
    import { goto } from "$app/navigation";

    let errorAnimation = spring(0, {
        stiffness: 0.3,
        damping: 0.2,
    });

    let usernameValue;
    let passwordValue;

    let privacyChecked = false;

    let error = false;
    let userData = null;

    async function submit() {
        userData = await singUp(usernameValue, passwordValue);

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

<main class="page page-center">
    {#if !userData}
        <form on:submit|preventDefault={() => submit()}>
            <div
                class="card text-center shadow-card w-full max-w-xl transform-gpu"
                style={`transform:translateX(${$errorAnimation}px);`}
            >
                <div class="card-body items-center">
                    <div class="py-2">
                        <h1 class="card-title">Sign up</h1>
                        <div>
                            Let’s set up your account, Already have one?<wbr />
                            <a class="link link-primary" href="/signin">
                                Sign in here.
                            </a>
                        </div>
                    </div>

                    <div class="form-control w-full">
                        <label for="username" class="label label-text"
                            >Username</label
                        >
                        <input
                            type="text"
                            name="username"
                            placeholder="username"
                            class="input input-bordered"
                            class:input-error={error}
                            bind:value={usernameValue}
                            on:input={unsetError}
                        />
                    </div>

                    <div class="form-control w-full">
                        <label for="password" class="label label-text"
                            >Password</label
                        >
                        <input
                            type="password"
                            name="password"
                            placeholder="password"
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
                        User already exist.
                    </div>
                    <div class="flex  py-4">
                        <input
                            type="checkbox"
                            name="privacy"
                            class="checkbox shrink-0"
                            bind:checked={privacyChecked}
                        />
                        <label for="privacy" class="text-xs ml-2 text-left">
                            I accept the Projectify Terms of Service. For more
                            information about Projectify's use and protection
                            of your data, please see our Privacy Policy.
                        </label>
                    </div>
                    <div class="pt-2">
                        <button
                            class="btn btn-primary rounded-full"
                            type="submit"
                            disabled={!privacyChecked}
                        >
                            Sign up
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
                    <h1 class="card-title">Email sent</h1>
                    <div>
                        I sent an email to <span class="link link-primary"
                            >{userData.email}</span
                        >. Please proceed from the url described in the
                        message.<wbr />
                    </div>
                </div>
                <div class="pt-2">
                    <button class="btn btn-primary" on:click={gotoTopPage}>
                        Top page
                    </button>
                </div>
            </div>
        </div>
    {/if}
</main>
