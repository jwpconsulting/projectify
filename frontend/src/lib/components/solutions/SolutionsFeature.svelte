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
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import type { FeatureDescription } from "$lib/types/ui";

    export let feature: FeatureDescription;
</script>

<section class="flex flex-col items-center gap-6 sm:grid sm:grid-cols-2">
    <div
        class={`flex flex-col gap-6 ${
            feature.image.position === "left" ? "sm:order-last" : ""
        }`}
    >
        <h4 class="text-xl font-bold sm:text-4xl">
            {feature.title}
        </h4>
        <p class="text-l">
            {feature.text}
        </p>
        {#if feature.learnMore !== undefined}
            <Anchor
                label={feature.learnMore.label}
                href={feature.learnMore.href}
            />
        {/if}
    </div>
    <div class="w-full max-w-xs justify-self-center">
        <img src={feature.image.src} alt={feature.image.alt} />
    </div>
</section>
