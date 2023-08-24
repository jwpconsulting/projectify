<script lang="ts">
    import type { PageData } from "./$types";

    import SettingsPage from "$lib/components/SettingsPage.svelte";
    import Overview from "$lib/figma/screens/user-account-settings/Overview.svelte";

    export let data: PageData;
    let { user } = data;
</script>

<SettingsPage title="My Profile">
    <Overview bind:user />
</SettingsPage>
