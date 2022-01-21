<script lang="ts">
    import {
        confirmPasswordReset,
        emailConfirmation,
        login,
    } from "$lib/stores/user";
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";

    let requestSent = false;
    let userData = null;
    let error = null;
    let passwordValue;

    let email = $page.params["email"];
    let token = $page.params["token"];

    async function submit() {
        userData = await confirmPasswordReset(email, token, passwordValue);

        if (userData && userData.error) {
            error = userData.error.message;
        } else {
            requestSent = true;
        }
    }

    function gotoTopPage() {
        goto("/");
    }
</script>

<main class="page page-center">
    {#if !requestSent}
        <form
            class="contents"
            action="/signup"
            method="post"
            on:submit|preventDefault={() => submit()}
        >
            <div class="card text-center shadow-card w-full max-w-xl">
                <div class="card-body items-center">
                    <div class="py-2">
                        <h1 class="card-title">Password reset</h1>
                        <div>
                            Please enter a your email to request a password
                            reset.
                        </div>
                    </div>

                    <div class="form-control w-full">
                        <label for="email" class="label label-text"
                            >Email</label
                        >
                        <input
                            type="password"
                            id="password"
                            autocomplete="new-password"
                            placeholder="Please enter a password"
                            class="input input-bordered"
                            class:input-error={error}
                            bind:value={passwordValue}
                            on:input={() => (error = null)}
                        />
                    </div>
                    <div
                        class="p-2  hi form-pop-msg text-error"
                        class:hidden={error == null}
                    >
                        {#if !passwordValue}
                            Password can not be empty.
                        {:else}
                            Something went wrong.
                        {/if}
                    </div>

                    <div class="pt-2">
                        <button
                            class="btn btn-primary rounded-full w-28 mt-4"
                            type="submit"
                        >
                            Send
                        </button>
                    </div>
                </div>
            </div>
        </form>
    {:else}
        <div class="card text-center shadow-card w-full max-w-lg">
            <div class="card-body items-center">
                <div class="py-2">
                    <h1 class="card-title">Password reset complete</h1>
                    <div class="text-left">
                        Your password has been changed, and you have been
                        logged into your account. Please continue to enjoy
                        Projectify.
                    </div>
                </div>

                <div class="pt-2">
                    <button
                        on:click={() => gotoTopPage()}
                        class="btn btn-primary rounded-full w-28 mt-4"
                    >
                        Top page
                    </button>
                </div>
            </div>
        </div>
    {/if}
</main>
