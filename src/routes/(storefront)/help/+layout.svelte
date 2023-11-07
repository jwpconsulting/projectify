<script lang="ts">
    import { _ } from "svelte-i18n";

    import HelpDropdown from "$lib/figma/dropdown/HelpDropdown.svelte";
</script>

<div class="flex h-full flex-col">
    <header class="bg-base-200 p-4">
        <div class="grid grid-cols-1 gap-4 sm:m-16 sm:grid-cols-2">
            <div>
                <h1 class="mb-8 text-4xl font-bold md:text-6xl">
                    {$_("help.hero-header")}
                </h1>
                <p class="mb-8 max-w-md text-2xl">
                    {$_("help.hero-text")}
                </p>
            </div>
            <div class="min-w-full max-w-md">
                <img src="/assets/help/help-hero.png" alt="TODO" />
            </div>
        </div>
    </header>
    <div class="flex grow flex-col gap-8 bg-foreground sm:px-12 md:flex-row">
        <HelpDropdown />
        <div class="flex flex-col bg-foreground p-8">
            <slot />
        </div>
    </div>
</div>
