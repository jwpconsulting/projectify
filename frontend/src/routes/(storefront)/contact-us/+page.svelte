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

    import Hero from "$lib/components/layouts/Hero.svelte";
    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import type { SolutionsHeroContent } from "$lib/types/ui";

    import Illustration from "./illustration.png";

    $: heroContent = {
        title: $_("contact-us.title"),
    } satisfies SolutionsHeroContent;
</script>

<HeroLayout>
    <Hero {heroContent} slot="hero" />
    <div
        slot="content"
        class="flex flex-row items-center justify-center gap-8"
    >
        <div class="flex max-w-xl flex-col gap-4">
            <h2 class="text-lg font-bold">
                {$_("contact-us.body.title")}
            </h2>
            <p>{$_("contact-us.body.text")}</p>
            <p>
                <Anchor
                    href={$_("contact-us.email.href")}
                    label={$_("contact-us.email.label")}
                />
            </p>
        </div>
        <div class="hidden shrink basis-1/4 md:block">
            <img src={Illustration} alt={$_("contact-us.illustration.alt")} />
        </div>
    </div>
</HeroLayout>
