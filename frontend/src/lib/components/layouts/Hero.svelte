<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    // Rename to just Hero and put in Layouts
    import type { SolutionsHeroContent } from "$lib/types/ui";

    export let heroContent: SolutionsHeroContent;
</script>

<header
    class="flex w-full flex-col items-center gap-4 {heroContent.image
        ? 'sm:grid sm:grid-cols-2'
        : ''}"
    class:justify-center={heroContent.image === undefined}
>
    <div
        class="flex flex-col gap-8 text-center font-bold {heroContent.image
            ? 'sm:text-left'
            : ''}"
        class:items-center={heroContent.image === undefined}
    >
        <h1 class="text-4xl lg:text-6xl">
            {heroContent.title}
        </h1>
        {#if heroContent.text}
            <p class="max-w-md text-xl">
                {heroContent.text}
            </p>
        {/if}
    </div>
    {#if heroContent.image}
        <div class="w-full max-w-xs justify-self-center">
            <enhanced:img
                src={heroContent.image.src}
                alt={heroContent.image.alt}
            />
        </div>
    {/if}
</header>
