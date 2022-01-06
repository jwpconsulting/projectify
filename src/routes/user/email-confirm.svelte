<script lang="ts">
    import { emailConfirmation, login } from "$lib/stores/user";
    import { goto } from "$app/navigation";
    import { page } from "$app/stores";
    import { onMount } from "svelte";

    let userData = null;
    let error;

    let email = $page.query.get("email");
    let token = $page.query.get("token");
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
        Loading
    {:else if error}
        <div
            class="card text-center shadow-card w-full max-w-xl transform-gpu"
        >
            <div class="card-body items-center">
                <div class="py-2">
                    <h1 class="card-title text-error">Error</h1>
                    <div>Something went wrong.</div>
                </div>
                <div class="pt-2">
                    <button class="btn btn-primary" on:click={gotoTopPage}>
                        Top page
                    </button>
                </div>
            </div>
        </div>
    {:else}
        <div
            class="card text-center shadow-card w-full max-w-xl transform-gpu"
        >
            <div class="card-body items-center">
                <div class="py-2">
                    <h1 class="card-title">Sign up finished</h1>
                    <div>
                        Sign up is finishied. Enjoy the application from now
                        on.
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
