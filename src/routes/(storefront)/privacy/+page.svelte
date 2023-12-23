<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";

    import PpEn from "./pp-en-formatted.svelte";
    import PpGdprEn from "./pp-gdpr-en-formatted.svelte";
    import PpGdprJa from "./pp-gdpr-ja-formatted.svelte";
    import PpJa from "./pp-ja-formatted.svelte";
</script>

<HeroLayout isProseContent={true}>
    <nav slot="side" class="flex max-w-xs grow flex-col gap-2">
        <p id="top" class="font-bold">{$_("privacy-policy.nav.title")}</p>
        <ol class="list-inside list-disc">
            <li>
                <Anchor
                    label={$_("privacy-policy.nav.japanese")}
                    href="#japanese"
                />
            </li>
            <li>
                <Anchor
                    label={$_("privacy-policy.nav.english")}
                    href="#english"
                />
            </li>
            <li>
                <Anchor
                    label={$_("privacy-policy.nav.japanese-gdpr")}
                    href="#japanese-gdpr"
                />
            </li>
            <li>
                <Anchor
                    label={$_("privacy-policy.nav.english-gdpr")}
                    href="#english-gdpr"
                />
            </li>
        </ol>
    </nav>
    <div
        slot="content"
        class="flex flex-col gap-10 sm:max-h-screen sm:overflow-y-auto"
    >
        <section class="prose" id="japanese">
            <PpJa />
        </section>
        <Anchor label={$_("privacy-policy.nav.go-back")} href="#top" />
        <section id="english" class="prose">
            <PpEn />
        </section>
        <Anchor label={$_("privacy-policy.nav.go-back")} href="#top" />
        <section class="prose" id="japanese-gdpr">
            <PpGdprJa />
        </section>
        <Anchor label={$_("privacy-policy.nav.go-back")} href="#top" />
        <section id="english-gdpr" class="prose">
            <PpGdprEn />
        </section>
        <Anchor label={$_("privacy-policy.nav.go-back")} href="#top" />
    </div>
</HeroLayout>
