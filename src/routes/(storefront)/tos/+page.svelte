<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";

    import TosEn from "./tos-en-formatted.svelte";
    import TosJa from "./tos-ja-formatted.svelte";
</script>

<HeroLayout isProseContent={true}>
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
    <div
        slot="content"
        class="flex flex-col gap-10 sm:max-h-screen sm:overflow-y-auto"
    >
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
