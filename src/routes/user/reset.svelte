<script lang="ts">
    import { goto } from "$app/navigation";
    import IllustrationEmailSent from "$lib/components/illustrations/illustration-email-sent.svelte";
    import { requestPasswordReset } from "$lib/stores/user";
    import { _ } from "svelte-i18n";

    let emailValue: string;
    let error: string | null = null;
    let requestSent = false;

    async function submit() {
        await requestPasswordReset(emailValue);
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
            <div class="card shadow-card w-full max-w-xl text-center">
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
                            >{$_("email")}</label
                        >
                        <input
                            type="email"
                            id="email"
                            autocomplete="email"
                            placeholder={$_("please-enter-your-email")}
                            class="input input-bordered"
                            class:input-error={error}
                            bind:value={emailValue}
                            on:input={() => (error = null)}
                        />
                    </div>
                    <div
                        class="hi  form-pop-msg p-2 text-error"
                        class:hidden={!error}
                    >
                        {$_("user-not-found")}
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
        <div class="card shadow-card w-full max-w-lg text-center">
            <div class="card-body items-center">
                <div class="py-2">
                    <div class="flex items-center justify-center pb-2">
                        <IllustrationEmailSent />
                    </div>
                    <h1 class="card-title">
                        {$_("password-reset-email-sent")}
                    </h1>
                    <div class="text-left">
                        {$_("i-sent-an-email-to")}
                        <span class="link link-primary">{emailValue}</span>.
                        {$_(
                            "please-proceed-from-the-url-described-in-the-message"
                        )}
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
