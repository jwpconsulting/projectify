<script lang="ts">
    import type { SolutionsHeroContent } from "$lib/types/ui";

    export let heroContent: SolutionsHeroContent;
</script>

<div class="flex w-full flex-col items-center bg-base-content p-6 sm:p-16">
    <div
        class="flex max-w-2xl flex-col items-center gap-4 sm:grid sm:grid-cols-2"
    >
        <div
            class="mb-8 flex flex-col gap-8 text-center font-bold text-foreground sm:text-left"
        >
            <h1 class="text-4xl">
                {heroContent.title}
            </h1>
            <p class="max-w-md text-xl">
                {heroContent.text}
            </p>
        </div>
        <div class="w-full max-w-xs">
            <img src={heroContent.image.src} alt={heroContent.image.alt} />
        </div>
    </div>
</div>
