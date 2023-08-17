<script lang="ts">
    import type { PageData } from "./$types";

    import SettingsPage from "$lib/components/SettingsPage.svelte";
    import UserAccountSettingsPage from "$lib/figma/screens/user-account-settings/UserAccountSettingsPage.svelte";

    export let data: PageData;
    let { user } = data;
</script>

<SettingsPage title="My Profile">
    <UserAccountSettingsPage bind:user />
</SettingsPage>
