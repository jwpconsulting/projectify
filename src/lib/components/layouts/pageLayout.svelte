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
            title: $_("service"),
            links: [
                {
                    name: $_("support"),
                    url: "/",
                },
                {
                    name: $_("policy"),
                    url: "/",
                },
                {
                    name: $_("terms"),
                    url: "/",
                },
            ],
        },
        {
            title: $_("company"),
            links: [
                {
                    name: $_("about"),
                    url: "/",
                },
                {
                    name: $_("blog"),
                    url: "/",
                },
                {
                    name: $_("contact"),
                    url: "/",
                },
                {
                    name: $_("legal"),
                    url: "/",
                },
            ],
        },
        {
            title: $_("social"),
            links: [
                {
                    name: "Github",
                    url: "/",
                },
                {
                    name: "Twitter",
                    url: "/",
                },
                {
                    name: "Instagram",
                    url: "/",
                },
            ],
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
            class="flex min-h-[200px] justify-center border-t border-base-300 bg-base-100 py-8 px-6"
        >
            <div
                class="container flex w-full flex-wrap items-start justify-between gap-y-4 gap-x-16 "
            >
                <div class="flex flex-col gap-4">
                    <HeaderLogo />
                    <div class="text-sm">
                        {$_("enable-smooth-project-management")}
                    </div>
                    <div class="flex gap-4">
                        {#each socials as social}
                            <a
                                href={social.url}
                                target="_blank"
                                class="btn btn-square border border-base-300 bg-[#fff]"
                            >
                                <svelte:component this={social.icon} />
                            </a>
                        {/each}
                    </div>
                </div>
                <div class="flex grow justify-between gap-8 sm:justify-start">
                    {#each footerLinks as group}
                        <div class="flex flex-col">
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
        </footer>
    {/if}
</div>
