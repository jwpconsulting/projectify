<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";
    import "$lib/app.scss";
    import faviconHtml from "favicon-html";

    const isDevelopment = __MODE__ === "development";
</script>

<svelte:head>
    <meta
        name="description"
        content="Projectify - Manage projects the right way"
    />
    <!-- This is statically generated, so we are good -->
    <!-- eslint-disable-next-line svelte/no-at-html-tags -->
    {@html faviconHtml}
</svelte:head>

<noscript>
    <section class="flex w-full flex-col gap-2 bg-destructive/30 p-4">
        <h1 class="text-center font-bold">
            {$_("navigation.header.noscript.body")}
        </h1>
        <p>{$_("navigation.header.noscript.personal-note")}</p>
    </section>
</noscript>

{#if isDevelopment}
    <p
        class="absolute left-0 top-0 w-full bg-destructive/30 text-center font-bold"
    >
        {$_("navigation.header.development-preview")}
    </p>
{/if}

<slot />
