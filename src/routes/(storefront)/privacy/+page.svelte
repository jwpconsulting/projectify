<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";

    import PpEn from "./pp-en-formatted.html?raw";
    import PpJa from "./pp-ja-formatted.html?raw";
</script>

<HeroLayout isProseContent={true}>
    <nav slot="side" class="flex max-w-xs flex-col gap-2">
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
        </ol>
    </nav>
    <div slot="content" class="flex flex-col gap-10">
        <section class="prose" id="japanese">
            <!-- eslint-disable-next-line svelte/no-at-html-tags -->
            {@html PpJa}
        </section>
        <Anchor label={$_("privacy-policy.nav.go-back")} href="#top" />
        <section id="english" class="prose">
            <!-- eslint-disable-next-line svelte/no-at-html-tags -->
            {@html PpEn}
        </section>
        <Anchor label={$_("privacy-policy.nav.go-back")} href="#top" />
    </div>
</HeroLayout>
