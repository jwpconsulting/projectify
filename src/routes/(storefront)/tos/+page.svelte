<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";

    import TosEn from "./tos-en-formatted.html?raw";
    import TosJa from "./tos-ja-formatted.html?raw";
</script>

<HeroLayout isProseContent={true}>
    <nav slot="side" class="flex max-w-xs flex-col gap-2">
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
            <!-- eslint-disable-next-line svelte/no-at-html-tags -->
            {@html TosJa}
        </section>
        <Anchor label={$_("terms-of-service.nav.go-back")} href="#top" />
        <section id="english" class="prose">
            <!-- eslint-disable-next-line svelte/no-at-html-tags -->
            {@html TosEn}
        </section>
        <Anchor label={$_("terms-of-service.nav.go-back")} href="#top" />
    </div>
</HeroLayout>
