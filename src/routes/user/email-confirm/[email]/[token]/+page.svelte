<script lang="ts">
    import { onMount } from "svelte";
    import { _ } from "svelte-i18n";
    import { emailConfirmation } from "$lib/stores/user";
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import IllustrationSignupFinish from "$lib/components/illustrations/illustration-signup-finish.svelte";
    import Loading from "$lib/components/loading.svelte";
    import type { User } from "$lib/types/user";

    let userData: User | null = null;
    let error: boolean;

    let email = $page.params["email"];
    let token = $page.params["token"];

    onMount(async () => {
        userData = await emailConfirmation(email, token);

        if (!userData) {
            error = true;
        }
    });

    function gotoTopPage() {
        goto("/");
    }
</script>

<main class="page page-center">
    {#if !userData && !error}
        <Loading />
    {:else if error}
        <div
            class="card w-full max-w-xl transform-gpu text-center shadow-card"
        >
            <div class="card-body items-center">
                <div class="py-2">
                    <h1 class="card-title text-error">{$_("error")}</h1>
                    <div>{$_("something-went-wrong")}</div>
                </div>
                <div class="pt-2">
                    <button class="btn btn-primary" on:click={gotoTopPage}>
                        {$_("top-page")}
                    </button>
                </div>
            </div>
        </div>
    {:else}
        <div
            class="card w-full max-w-xl transform-gpu text-center shadow-card"
        >
            <div class="card-body items-center">
                <div class="py-2">
                    <div class="flex items-center justify-center pb-2">
                        <IllustrationSignupFinish />
                    </div>
                    <h1 class="card-title">{$_("sign-up-finished")}</h1>
                    <div>
                        {$_("sign-up-is-finishied-msg")}
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
