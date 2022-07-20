<script lang="ts">
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import { _ } from "svelte-i18n";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { ChevronDown } from "@steeze-ui/heroicons";

    let navItems = [
        {
            title: $_("help.basics"),
            href: "/help/basics",
        },
        {
            title: $_("help.workspaces"),
            href: "/help/workspaces",
        },
        {
            title: $_("help.boards"),
            href: "/help/boards",
        },
        {
            title: $_("help.sections"),
            href: "/help/sections",
        },
        {
            title: $_("help.tasks"),
            href: "/help/tasks",
        },
        {
            title: $_("help.labels"),
            href: "/help/labels",
        },
        {
            title: $_("help.members"),
            href: "/help/members",
        },
        {
            title: $_("help.bulk-select"),
            href: "/help/bulk-select",
        },
        {
            title: $_("help.filters"),
            href: "/help/filters",
        },
        {
            title: $_("help.notifications"),
            href: "/help/notifications",
        },
        {
            title: $_("help.pop-ups"),
            href: "/help/pop-ups",
        },
        {
            title: $_("help.billing"),
            href: "/help/billing",
        },
    ];
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
            <div class="flex flex-col sm:m-6 sm:grid-cols-2 sm:pr-12">
                <aside
                    class="text-base-content sm:mt-4 sm:w-64"
                    aria-label="Sidebar"
                >
                    <button
                        id="dropdown-button"
                        class="flex w-full items-center p-4 text-xl font-bold"
                    >
                        <p class="ml-3 flex-1 text-left">Table of contents</p>
                        <Icon
                            src={ChevronDown}
                            theme="outline"
                            class="h-4 w-4"
                        />
                    </button>
                    <ul
                        id="dropdown-menu"
                        class="contenthidden space-y-2 py-2 sm:border-r "
                    >
                        {#each navItems as navItem}
                            <li>
                                <a
                                    href={navItem.href}
                                    class="flex items-center p-2"
                                >
                                    <p
                                        class="ml-8 flex-1 font-bold text-primary"
                                    >
                                        {navItem.title}
                                    </p>
                                </a>
                            </li>
                        {/each}
                    </ul>
                </aside>
                <slot />
            </div>
        </div>
    </main>
</PageLayout>
