<script lang="ts">
    import { _ } from "svelte-i18n";

    import HelpDropdown from "$lib/figma/dropdown/HelpDropdown.svelte";
</script>

<div class="flex h-full flex-col">
    <header class="bg-background px-4 py-8 md:px-16">
        <div class="flex flex-col gap-4 sm:grid-cols-2 md:grid">
            <heading class="flex flex-col gap-4">
                <h1 class="text-4xl font-bold md:text-6xl">
                    {$_("help.hero.header.text")}
                </h1>
                <p class="max-w-md text-2xl">
                    {$_("help.hero.header.subtext")}
                </p>
            </heading>
            <div class="min-w-full max-w-md">
                <img
                    src="/assets/help/help-hero.png"
                    alt={$_("help.hero.image.alt")}
                />
            </div>
        </div>
    </header>
    <main
        class="flex grow flex-col gap-4 bg-foreground px-4 py-2 sm:flex-row sm:gap-8 sm:p-8 sm:px-12"
    >
        <div class="grow">
            <HelpDropdown />
        </div>
        <div class="flex flex-col gap-7 bg-foreground">
            <slot />
        </div>
    </main>
</div>
