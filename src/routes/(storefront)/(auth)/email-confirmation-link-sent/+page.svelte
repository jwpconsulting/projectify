<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";

    import illustration from "./illustration.svg";
</script>

<div class="flex h-full flex-col items-center justify-center px-16 py-8">
    <div class="flex flex-col items-center gap-12">
        <h1 class="text-center text-4xl font-bold">
            {$_("auth.confirmation-link-sent.header")}
        </h1>
        <img
            src={illustration}
            alt={$_("auth.confirmation-link-sent.illustration-alt")}
        />
        <p>{$_("auth.confirmation-link-sent.body")}</p>
        <Button
            label={$_("auth.confirmation-link-sent.back-to-homepage")}
            size="medium"
            style={{ kind: "primary" }}
            color="blue"
            action={{ kind: "a", href: "/" }}
        />
    </div>
</div>
