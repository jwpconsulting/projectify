<script lang="ts">
    import { _ } from "svelte-i18n";

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
</script>

<div class="flex flex-col gap-12 p-20">
    <header class="flex flex-col gap-12">
        <h1 class="text-5xl font-bold">
            {$_("page404.title")}
        </h1>
        <p class="text-xl font-bold">
            {$_("page404.body")}
        </p>
    </header>
    <section>
        <Anchor label={$_("page404.home")} href="/" size="large" />
    </section>
</div>
