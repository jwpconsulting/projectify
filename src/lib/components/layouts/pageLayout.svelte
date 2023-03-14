<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeaderLogo from "$lib/components/assets/headerLogo.svelte";
    import Header from "$lib/components/Header.svelte";
    import IconGithub from "$lib/components/icons/icon-github.svelte";
    import IconInstagram from "$lib/components/icons/icon-instagram.svelte";
    import IconTwitter from "$lib/components/icons/icon-twitter.svelte";

    export let footerVisible = true;
    export let heightScreen = false;

    export let headerMode: "app" | "landing" = "app";

    let socials = [
        {
            icon: IconTwitter,
            url: "https://twitter.com",
        },
        {
            icon: IconInstagram,
            url: "https://instagram.com",
        },
        {
            icon: IconGithub,
            url: "https://github.com",
        },
    ];

    let footerLinks = [
        {
            title: $_("product"),
            links: [
                {
                    name: $_("features"),
                    url: "/",
                },
                {
                    name: $_("solutions"),
                    url: "/solutions",
                },
                {
                    name: $_("pricing"),
                    url: "/pricing",
                },
            ],
        },
        {
            title: $_("resources"),
            links: [
                {
                    name: $_("help-and-tips"),
                    url: "/help/basics",
                },
            ],
        },
        {
            title: $_("company"),
            links: [
                {
                    name: $_("about-us"),
                    url: "/",
                },
                {
                    name: $_("careers"),
                    url: "/",
                },
                {
                    name: $_("accessibility-statement"),
                    url: "/accessibility",
                },
                {
                    name: $_("contact-us"),
                    url: "/",
                },
            ],
        },
    ];

    const footerBottomLinks = [
        {
            name: $_("privacy"),
            url: "/",
        },
        {
            name: $_("terms"),
            url: "/",
        },
    ];
</script>

<div class:h-screen={heightScreen} class="flex grow flex-col">
    <Header bind:mode={headerMode} />
    <slot />
    {#if footerVisible}
        <footer
            class="flex min-h-[200px] justify-center border-t border-base-300"
        >
            {#if import.meta.env.DEV}
                <a href="/storybook/">Storybook</a>
            {/if}
            <div
                class="container flex w-full flex-wrap items-start justify-between"
            >
                <!-- Top row -->
                <div
                    class="flex w-full flex-wrap items-start justify-between gap-y-4 gap-x-16 py-8"
                >
                    <div class="flex flex-col gap-4">
                        <HeaderLogo />
                        <div class="text-sm">
                            {$_("project-management-at-pace")}
                        </div>
                        <div class="grow" />
                        <a href={"/"} class="btn btn-primary btn-md max-w-fit"
                            >{$_("start-a-free-trial")}</a
                        >
                    </div>

                    <div
                        class="flex grow justify-between gap-8 sm:justify-start"
                    >
                        {#each footerLinks as group}
                            <div class="flex flex-col gap-2">
                                <h1 class="font-bold">{group.title}</h1>
                                {#each group.links as link}
                                    <a class="link text-sm" href={link.url}
                                        >{link.name}</a
                                    >
                                {/each}
                            </div>
                        {/each}
                    </div>
                </div>

                <!-- Bottom row -->
                <div class="flex grow items-center border-t py-6">
                    <!-- Left -->
                    <div class="flex grow gap-4">
                        {#each footerBottomLinks as link}
                            <a class="link text-sm" href={link.url}
                                >{link.name}</a
                            >
                        {/each}
                    </div>
                    <!-- Right -->
                    <div>
                        <div class="flex gap-8">
                            {#each socials as social}
                                <a
                                    href={social.url}
                                    target="_blank"
                                    rel="noreferrer"
                                    class="shrink-0 text-base-content"
                                >
                                    <svelte:component this={social.icon} />
                                </a>
                            {/each}
                        </div>
                    </div>
                </div>
            </div>
        </footer>
    {/if}
</div>
