<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Anchor from "$lib/funabashi/typography/Anchor.svelte";

    import { page } from "$app/stores";

    $: errorMessage = $page.error?.message ?? $_("dashboard.error.title");
</script>

<div class="flex flex-col gap-6 p-16">
    <header class="flex flex-col gap-4">
        <h1 class="text-3xl font-bold">
            {errorMessage}
        </h1>
    </header>
    <main class="flex flex-col gap-4">
        <p>
            {$_("dashboard.error.description")}
        </p>
        <code>
            {errorMessage}
        </code>
        <p>
            {$_("dashboard.error.what-to-do.message")}
        </p>
        <ol class="list-inside list-disc">
            <li>
                <Anchor
                    href="/help"
                    label={$_("dashboard.error.what-to-do.options.help")}
                    size="normal"
                    openBlank
                />
            </li>
            <li>
                <Anchor
                    href="/contact-us"
                    label={$_("dashboard.error.what-to-do.options.contact-us")}
                    size="normal"
                    openBlank
                />
            </li>
        </ol>
    </main>
</div>
