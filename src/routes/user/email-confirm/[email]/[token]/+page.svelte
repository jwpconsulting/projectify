<script lang="ts">
    import { _ } from "svelte-i18n";
    import { goto } from "$app/navigation";
    import IllustrationSignupFinish from "$lib/components/illustrations/illustration-signup-finish.svelte";

    function gotoTopPage() {
        goto("/");
    }
</script>

<div class="card w-full max-w-xl transform-gpu text-center shadow-card">
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
