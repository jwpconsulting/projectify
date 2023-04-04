<script lang="ts">
    import { page } from "$app/stores";
    import { user } from "$lib/stores/user";
    import routes from "$lib/routes";
    import { _ } from "svelte-i18n";
    import HeaderLogo from "$lib/components/assets/headerLogo.svelte";
    import HeaderUser from "$lib/components/headerUser.svelte";
    import IconHamburgerMenu from "$lib/components/icons/icon-hamburger-menu.svelte";
    import HeaderButtons from "$lib/components/header-buttons.svelte";
    import BoardSearchBar from "$lib/components/BoardSearchBar.svelte";

    export let mode = "app";

    type HeaderItem = {
        label: string;
        to?: string;
        authRequired?: boolean;
        forceNaviagiation?: boolean;
        fetchUser?: boolean;
        action?: (arg0: any) => void;
    };

    let items: HeaderItem[] = [];

    $: userData = $user;
    $: {
        if (mode == "landing") {
            items = [
                {
                    label: $_("product"),
                    to: "/",
                },
                {
                    label: $_("resources"),
                    to: "/",
                },
                {
                    label: $_("pricing"),
                    to: "/",
                },
            ];
        } else {
            items = [...routes]
                .filter((it) => {
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
                })
                .map((it) => ({
                    ...it,
                    label: $_(it.label),
                }));
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
                                class="cursor-pointer p-2 font-bold capitalize"
                                href={it.to}
                            >
                                {it.label}
                            </a>
                        </li>
                    {/each}
                </ul>
            </nav>
            <div class="grow" />
            <nav class="hidden gap-2 md:flex">
                <HeaderButtons {userData} />
            </nav>

            <button
                on:click={() => (drawerMenuOpen = true)}
                class="flex  h-10 w-10 shrink-0 items-center justify-center self-end rounded-full bg-base-100 text-primary md:hidden"
                ><IconHamburgerMenu /></button
            >
        </div>
    </header>
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
                            class="cursor-pointer p-2 font-bold capitalize"
                            href={it.to}
                        >
                            {it.label}
                        </a>
                    </li>
                {/each}
            </ul>
        </nav>

        <div class="flex flex-row items-center gap-7">
            <BoardSearchBar />
            <HeaderUser />
        </div>
    </header>
{/if}
