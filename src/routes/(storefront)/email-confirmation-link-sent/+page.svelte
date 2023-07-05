<script lang="ts">
    import { _ } from "svelte-i18n";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import illustration from "./illustration.svg";
</script>

<div class="flex h-full flex-col items-center justify-center">
    <div class="flex flex-col items-center gap-12">
        <h1 class="text-4xl font-bold">
            {$_("sign-up.confirmation-link-sent.header")}
        </h1>
        <img
            src={illustration}
            alt={$_("sign-up.confirmation-link-sent.illustration-alt")}
        />
        <p>{$_("sign-up.confirmation-link-sent.body")}</p>
        <Button
            label={$_("sign-up.confirmation-link-sent.back-to-homepage")}
            size="medium"
            style={{ kind: "primary" }}
            color="blue"
            action={{ kind: "a", href: "/" }}
        />
    </div>
</div>
