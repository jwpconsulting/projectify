<script lang="ts">
    // TODO can this component be deleted?
    import { _ } from "svelte-i18n";

    import routes from "$lib/routes";

    import { page } from "$app/stores";
    import HeaderUser from "$lib/components/headerUser.svelte";
    import IconHamburgerMenu from "$lib/components/icons/icon-hamburger-menu.svelte";
    import { user } from "$lib/stores/user";

    export let mode = "app";

    interface HeaderItem {
        label: string;
        to?: string;
        authRequired?: boolean;
        forceNaviagiation?: boolean;
        fetchUser?: boolean;
        action?: () => void;
    }

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
</script>

<svelte:window bind:scrollY />

{#if mode == "landing"}
    <header
        class="sticky top-0 z-10 flex h-[80px] items-center justify-center bg-base-100 px-6 transition-all duration-300 ease-in-out"
        class:lg:bg-transparent={scrollToTop}
        class:shadow-lg={!scrollToTop}
    >
        <div class="container flex items-center">
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

            <button
                class="flex h-10 w-10 shrink-0 items-center justify-center self-end rounded-full bg-base-100 text-primary md:hidden"
                ><IconHamburgerMenu /></button
            >
        </div>
    </header>
{:else}
    <header
        class="sticky top-0 z-10 flex h-[80px] items-center border-b border-base-300 bg-base-100 p-4"
    >
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
            <HeaderUser />
        </div>
    </header>
{/if}
