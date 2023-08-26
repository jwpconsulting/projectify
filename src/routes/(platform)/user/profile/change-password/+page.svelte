<script lang="ts">
    import type { PageData } from "./$types";

    import UserAccountSettings from "$lib/figma/screens/user-account-settings/UserAccountSettings.svelte";

    export let data: PageData;
    let { user } = data;
</script>

<UserAccountSettings bind:user mode="change-password" />
