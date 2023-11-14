<script lang="ts">
    import ConfirmPasswordReset from "$lib/figma/screens/auth/ConfirmPasswordReset.svelte";

    import type { PageData } from "./$types";

    export let data: PageData;

    const { email, token } = data;
</script>

<ConfirmPasswordReset {email} {token} />
