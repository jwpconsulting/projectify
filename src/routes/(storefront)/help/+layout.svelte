<script lang="ts">
    import { _ } from "svelte-i18n";

    import HelpDropdown from "$lib/figma/dropdown/HelpDropdown.svelte";
</script>

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
<div class="flex flex-row gap-8 bg-foreground sm:my-6 sm:flex sm:px-12">
    <HelpDropdown />
    <slot />
</div>
