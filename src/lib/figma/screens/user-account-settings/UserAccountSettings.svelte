<script lang="ts">
    import { _ } from "svelte-i18n";

    import Overview from "$lib/figma/screens/user-account-settings/Overview.svelte";
    import type { User } from "$lib/types/user";

    export let user: User;
</script>

<div class="flex flex-col gap-4">
    <h1 class="text-2xl font-bold">
        {$_("user-account-settings.title")}
    </h1>
    <Overview {user} />
</div>
