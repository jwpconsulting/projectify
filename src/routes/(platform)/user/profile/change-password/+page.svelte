<script lang="ts">
    import ChangePassword from "$lib/figma/screens/user-account-settings/ChangePassword.svelte";

    import type { PageData } from "./$types";

    export let data: PageData;
    const { user } = data;
</script>

<ChangePassword {user} />
