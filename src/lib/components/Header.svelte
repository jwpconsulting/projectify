<script lang="ts">
    import { page } from "$app/stores";
    import { user, logout } from "$lib/stores/user";
    import routes from "$lib/routes";
    import { _ } from "svelte-i18n";
    import HeaderLogo from "./assets/headerLogo.svelte";
    import HeaderUser from "./headerUser.svelte";
    import { onMount } from "svelte";
    import IconHamburgerMenu from "./icons/icon-hamburger-menu.svelte";
    import DrawerModal from "./drawerModal.svelte";
    import IconClose from "./icons/icon-close.svelte";

    export let mode = "app";
    let items;
    $: userData = $user;
    $: {
        if (mode == "landing") {
            items = [
                {
                    label: "Problem",
                    to: "/#problem",
                },
                {
                    label: "Solution",
                    to: "/#solution",
                },
                {
                    label: "Github",
                    to: "/#github",
                },
            ];
        } else {
            items = [...routes].filter((it) => {
                if (it.forceNavigation) {
                    return true;
                }

                if (it.forceNavigation === false) {
                    return false;
                }

                if (!userData && it.authRequired === true) {
                    return false;
                }

                if (userData && it.authRequired === false) {
                    return false;
                }

                return true;
            });
        }
    }

    let scrollY = 0;
    $: scrollToTop = scrollY < 20;

    let drawerMenuOpen = false;
</script>

<svelte:window bind:scrollY />

{#if mode == "landing"}
    <header
        class="sticky top-0 z-10 flex h-[80px] items-center justify-center bg-base-100 px-6 transition-all duration-300 ease-in-out"
        class:lg:bg-transparent={scrollToTop}
        class:shadow-lg={!scrollToTop}
    >
        <div class="container flex items-center">
            <a href="/" class="mr-8 flex">
                <HeaderLogo />
            </a>
            <nav class="hidden grow md:flex">
                <ul class="flex">
                    {#each items as it}
                        <li class:active={$page.url.pathname === it.to}>
                            <a
                                on:click={it.action}
                                class="cursor-pointer p-2 font-bold"
                                href={it.to}
                            >
                                {$_(it.label)}
                            </a>
                        </li>
                    {/each}
                </ul>
            </nav>
            <div class="grow" />
            <nav class="hidden gap-2 md:flex">
                <a
                    href="/signin"
                    class="btn btn-outline btn-primary rounded-full bg-base-100 px-8 capitalize"
                    >Signin</a
                >
                <a
                    href="/signup"
                    class="btn btn-primary rounded-full px-8 capitalize"
                    >Signup</a
                >
            </nav>

            <button
                on:click={() => (drawerMenuOpen = true)}
                class="flex  h-10 w-10 shrink-0 items-center justify-center self-end rounded-full bg-base-100 text-primary md:hidden"
                ><IconHamburgerMenu /></button
            >
        </div>
    </header>

    <DrawerModal bind:open={drawerMenuOpen}>
        <div class="flex min-h-[100%] min-w-[100vw] flex-col gap-6 p-6">
            <div class="flex ">
                <a href="/" class="mr-8 flex grow">
                    <HeaderLogo />
                </a>

                <button
                    on:click={() => (drawerMenuOpen = false)}
                    class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-base-100 text-primary"
                    ><IconClose />
                </button>
            </div>
            <nav class="flex grow flex-col">
                <ul class="flex flex-col divide-y divide-base-300">
                    {#each items as it}
                        <li
                            class="flex text-xl"
                            class:active={$page.url.pathname === it.to}
                        >
                            <a
                                on:click={() => {
                                    drawerMenuOpen = false;
                                }}
                                class="cursor-pointer p-2 font-bold"
                                href={it.to}
                            >
                                {$_(it.label)}
                            </a>
                        </li>
                    {/each}
                </ul>
            </nav>
            <div class="grow" />
            <nav class="flex flex-col gap-2">
                <a
                    href="/signin"
                    class="btn btn-outline btn-primary rounded-full bg-base-100 px-8 capitalize"
                    >Signin</a
                >
                <a
                    href="/signup"
                    class="btn btn-primary rounded-full px-8 capitalize"
                    >Signup</a
                >
            </nav>
        </div>
    </DrawerModal>
{:else}
    <header
        class="sticky top-0 z-10 flex h-[80px] items-center border-b border-base-300 bg-base-100 p-4"
    >
        <a href="/" class="mr-8 flex">
            <HeaderLogo />
        </a>
        <nav class="grow">
            <ul class="flex">
                {#each items as it}
                    <li class:active={$page.url.pathname === it.to}>
                        <a
                            on:click={it.action}
                            class="cursor-pointer p-2 font-bold"
                            href={it.to}
                        >
                            {$_(it.label)}
                        </a>
                    </li>
                {/each}
            </ul>
        </nav>

        <HeaderUser />
    </header>
{/if}
