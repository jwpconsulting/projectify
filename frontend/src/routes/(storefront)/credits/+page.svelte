<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";

    import Vendored from "../../../../LICENSES/MIT.txt?raw";
    import ThirdParty from "third-party-licenses";
</script>

<svelte:head>
    <title>{$_("credits.title")}</title>
</svelte:head>

<HeroLayout heroBackground>
    <div slot="hero">
        <h1 class="text-3xl font-bold">{$_("credits.hero")}</h1>
    </div>
    <div slot="content" class="prose">
        <p>{$_("credits.body")}</p>
        <h2>{$_("credits.vendored")}</h2>
        <pre>{Vendored}</pre>
        <h2>{$_("credits.npm")}</h2>
        <pre>{ThirdParty}</pre>
    </div>
</HeroLayout>
