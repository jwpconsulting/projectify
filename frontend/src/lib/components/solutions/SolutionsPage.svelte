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
    import Hero from "$lib/components/layouts/Hero.svelte";
    import HeroLayout from "$lib/components/layouts/HeroLayout.svelte";
    import SolutionsFeature from "$lib/components/solutions/SolutionsFeature.svelte";
    import type { SolutionsPageContent } from "$lib/types/ui";

    export let pageContent: SolutionsPageContent;
</script>

<HeroLayout>
    <Hero slot="hero" heroContent={pageContent.heroContent} />

    <div
        slot="content"
        class="flex w-full flex-col items-center gap-6 sm:gap-16"
    >
        {#each pageContent.features as feature}
            <SolutionsFeature {feature} />
        {/each}
    </div>
</HeroLayout>
