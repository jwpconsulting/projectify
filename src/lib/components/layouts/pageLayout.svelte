<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeaderLogo from "../assets/headerLogo.svelte";
    import Header from "../Header.svelte";
    import IconGithub from "../icons/icon-github.svelte";
    import IconInstagram from "../icons/icon-instagram.svelte";
    import IconTwitter from "../icons/icon-twitter.svelte";

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
            title: "Product",
            links: [
                {
                    name: "Features",
                    url: "/",
                },
                {
                    name: "Solutions",
                    url: "/",
                },
                {
                    name: "Pricing",
                    url: "/",
                },
            ],
        },
        {
            title: "Resources",
            links: [
                {
                    name: "Help and tips",
                    url: "/",
                },
            ],
        },
        {
            title: $_("company"),
            links: [
                {
                    name: "About us",
                    url: "/",
                },
                {
                    name: "Careers",
                    url: "/",
                },
                {
                    name: "Accessibility statement",
                    url: "/",
                },
                {
                    name: "Contact us",
                    url: "/",
                },
            ],
        },
    ];

    const footerBottomLinks = [
        {
            name: "Privacy",
            url: "/",
        },
        {
            name: $_("terms"),
            url: "/",
        },
    ];
</script>

<div
    class:h-screen={heightScreen}
    class:overflow-hidden={heightScreen}
    class="flex grow flex-col"
>
    <Header bind:mode={headerMode} />
    <slot />
    {#if footerVisible}
        <footer
            data-theme="app-dark"
            class="flex min-h-[200px] justify-center border-t border-base-300  bg-[#002332] px-6 text-base-content"
        >
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
                            {"Project management at pace."}
                        </div>
                        <div class="grow" />
                        <a
                            href={"/"}
                            class="btn btn-primary btn-md max-w-fit rounded-full"
                            >{"Start a free trial"}</a
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
