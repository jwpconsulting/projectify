<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/components/solutions/Layout.svelte";
    import HelpDropdown from "$lib/figma/dropdown/HelpDropdown.svelte";
</script>

<Layout>
    <div slot="hero" class="flex flex-col gap-4 sm:grid-cols-2 md:grid">
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
    <div slot="side" class="grow">
        <HelpDropdown />
    </div>
    <div slot="content" class="flex flex-col gap-4">
        <slot />
    </div>
</Layout>
