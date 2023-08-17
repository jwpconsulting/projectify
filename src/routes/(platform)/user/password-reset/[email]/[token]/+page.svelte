<script lang="ts">
    import { _ } from "svelte-i18n";

    import { goto } from "$lib/navigation";

    import { page } from "$app/stores";
    import IllustrationPasswordResetComplete from "$lib/components/illustrations/illustration-password-reset-complete.svelte";
    import { confirmPasswordReset } from "$lib/stores/user";

    let requestSent = false;
    let error: string | null = null;
    let passwordValue: string;

    let email = $page.params.email;
    let token = $page.params.token;

    async function submit() {
        await confirmPasswordReset(email, token, passwordValue);
        requestSent = true;
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
            <div class="card w-full max-w-xl text-center shadow-card">
                <div class="card-body items-center">
                    <div class="py-2">
                        <h1 class="card-title">{$_("password-reset")}</h1>
                        <div>
                            {$_(
                                "please-enter-your-email-to-request-a-password-reset"
                            )}
                        </div>
                    </div>

                    <div class="form-control w-full">
                        <label for="email" class="label label-text"
                            >{$_("password")}</label
                        >
                        <input
                            type="password"
                            id="password"
                            autocomplete="new-password"
                            placeholder={$_("please-enter-a-password")}
                            class="input input-bordered"
                            class:input-error={error}
                            bind:value={passwordValue}
                            on:input={() => (error = null)}
                        />
                    </div>
                    <div
                        class="hi form-pop-msg p-2 text-error"
                        class:hidden={error == null}
                    >
                        {#if !passwordValue}
                            {$_("password-can-not-be-empty")}
                        {:else}
                            {$_("something-went-wrong")}
                        {/if}
                    </div>

                    <div class="pt-2">
                        <button
                            class="btn btn-primary mt-4 w-28 rounded-full"
                            type="submit"
                        >
                            {$_("send")}
                        </button>
                    </div>
                </div>
            </div>
        </form>
    {:else}
        <div class="card w-full max-w-lg text-center shadow-card">
            <div class="card-body items-center">
                <div class="py-2">
                    <div class="flex items-center justify-center pb-2">
                        <IllustrationPasswordResetComplete />
                    </div>
                    <h1 class="card-title">{$_("password-reset-complete")}</h1>
                    <div class="text-left">
                        {$_("user-password-reset-completed-msg")}
                    </div>
                </div>

                <div class="pt-2">
                    <button
                        on:click={() => gotoTopPage()}
                        class="btn btn-primary mt-4 w-28 rounded-full"
                    >
                        {$_("top-page")}
                    </button>
                </div>
            </div>
        </div>
    {/if}
</main>
