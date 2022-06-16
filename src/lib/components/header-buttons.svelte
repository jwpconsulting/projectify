<script lang="ts">
    import { _ } from "svelte-i18n";

    export let userData;
</script>

{#if userData}
    <a href="/dashboard" class="btn btn-primary btn-md rounded-full"
        >{$_("continue-to-dashboard")}</a
    >
{:else}
    <a
        href="/signin"
        class="btn btn-ghost text-primary btn-primary btn-md rounded-full bg-base-100"
        >{$_("log-in")}</a
    >
    <a href="/signup" class="btn btn-primary rounded-full btn-md"
        >{$_("start-a-free-trial")}</a
    >
{/if}
