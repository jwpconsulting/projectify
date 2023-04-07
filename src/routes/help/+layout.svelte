<script lang="ts">
    import { _ } from "svelte-i18n";
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import HelpDropdown from "$lib/figma/dropdown/HelpDropdown.svelte";
</script>

<PageLayout headerMode={"landing"}>
    <main class="page bg-base-100">
        <div>
            <div class="page bg base-200">
                <div class="m-6 grid grid-cols-1 gap-4 sm:m-16 sm:grid-cols-2">
                    <div class="/">
                        <h1 class="mb-8 text-4xl font-bold md:text-6xl">
                            {$_("help.hero-header")}
                        </h1>
                        <p class="mb-8 max-w-md text-2xl">
                            {$_("help.hero-text")}
                        </p>
                    </div>
                    <div class="min-w-full max-w-md">
                        <img src="/assets/help/help-hero.png" alt="" />
                    </div>
                </div>
            </div>
        </div>
        <div class="flex-row space-y-8 sm:my-6 sm:flex sm:px-12">
            <div>
                <HelpDropdown />
            </div>
            <slot />
        </div>
    </main>
</PageLayout>
