<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";

    import TosEn from "./tos-en-formatted.svelte";
    import TosJa from "./tos-ja-formatted.svelte";
</script>

<svelte:head>
    <title>{$_("terms-of-service.title")}</title>
</svelte:head>

<HeroLayout isProseContent heroBackground>
    <nav slot="side" class="flex max-w-xs grow flex-col gap-2">
        <p id="top" class="font-bold">{$_("terms-of-service.nav.title")}</p>
        <ol class="list-inside list-disc">
            <li>
                <Anchor
                    label={$_("terms-of-service.nav.japanese")}
                    href="#japanese"
                />
            </li>
            <li>
                <Anchor
                    label={$_("terms-of-service.nav.english")}
                    href="#english"
                />
            </li>
        </ol>
    </nav>
    <div slot="content" class="flex flex-col gap-10">
        <section class="prose" id="japanese">
            <TosJa />
        </section>
        <Anchor label={$_("terms-of-service.nav.go-back")} href="#top" />
        <section id="english" class="prose">
            <!-- eslint-disable-next-line svelte/no-at-html-tags -->
            <TosEn />
        </section>
        <Anchor label={$_("terms-of-service.nav.go-back")} href="#top" />
    </div>
</HeroLayout>
