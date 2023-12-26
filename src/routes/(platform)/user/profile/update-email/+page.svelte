<script lang="ts">
    import UpdateEmail from "$lib/figma/screens/user-account-settings/UpdateEmail.svelte";

    import type { PageData } from "./$types";

    export let data: PageData;
    const { user } = data;
</script>

<UpdateEmail {user} />
