<script lang="ts">
    import { goto } from "$app/navigation";
    import { requestPasswordReset } from "$lib/stores/user";
    import { _ } from "svelte-i18n";

    let emailValue;
    let error = null;
    let requestSent = false;

    async function submit() {
        const res = await requestPasswordReset(emailValue);

        if (res.error) {
            error = res.error.message;
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
                        <h1 class="card-title">{$_("password-reset")}</h1>
                        <div>
                            {$_("page-user-reset-msg")}
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
                        class="p-2  hi form-pop-msg text-error"
                        class:hidden={!error}
                    >
                        {$_("user-not-found")}
                    </div>

                    <div class="pt-2">
                        <button
                            class="btn btn-primary rounded-full w-28 mt-4"
                            type="submit"
                        >
                            {$_("send")}
                        </button>
                    </div>
                </div>
            </div>
        </form>
    {:else}
        <div class="card text-center shadow-card w-full max-w-lg">
            <div class="card-body items-center">
                <div class="py-2">
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
                        class="btn btn-primary rounded-full w-28 mt-4"
                    >
                        {$_("top-page")}
                    </button>
                </div>
            </div>
        </div>
    {/if}
</main>
