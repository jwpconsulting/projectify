<script lang="ts">
    import { _ } from "svelte-i18n";

    import ChangePassword from "$lib/figma/screens/user-account-settings/ChangePassword.svelte";
    import Overview from "$lib/figma/screens/user-account-settings/Overview.svelte";
    import UpdateEmail from "$lib/figma/screens/user-account-settings/UpdateEmail.svelte";
    import type { User } from "$lib/types/user";

    export let user: User;

    export let mode: "overview" | "change-password" | "update-email" =
        "overview";
</script>

<div class="flex flex-col gap-4">
    <h1 class="text-2xl font-bold">
        {$_("user-account-settings.title")}
    </h1>
    <div class="flex flex-col gap-12 rounded-lg bg-foreground p-4">
        {#if mode === "overview"}
            <Overview {user} />
        {:else if mode === "change-password"}
            <ChangePassword {user} />
        {:else if mode === "update-email"}
            <UpdateEmail {user} />
        {/if}
    </div>
</div>
