<script lang="ts">
    import { _ } from "svelte-i18n";

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { backToHomeUrl } from "$lib/urls";
    import { logInUrl } from "$lib/urls/user";
</script>

<div class="flex flex-col gap-8 px-8 py-8">
    <h1 class="text-center text-xl font-bold">{$_("auth.logout.success")}</h1>
    <p>
        <Anchor
            size="normal"
            label={$_("auth.logout.log-back-in")}
            href={logInUrl}
        />
    </p>
    <p>
        <Anchor
            size="normal"
            label={$_("auth.logout.landing")}
            href={backToHomeUrl}
        />
    </p>
</div>
