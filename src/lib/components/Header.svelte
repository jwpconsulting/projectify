<script lang="ts">
    import { page } from "$app/stores";
    import { user, logout } from "$lib/stores/user";
    import routes from "$lib/routes";
    import { _ } from "svelte-i18n";
    import HeaderLogo from "./assets/headerLogo.svelte";
    import HeaderUser from "./headerUser.svelte";
    import { onMount } from "svelte";

    export let mode = "app";
    let items;
    $: userData = $user;
    $: {
        if (mode == "landing") {
            items = [
                {
                    label: "Problem",
                    to: "#problem",
                },
                {
                    label: "Solution",
                    to: "#solution",
                },
                {
                    label: "Github",
                    to: "#github",
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
</script>

<svelte:window bind:scrollY />

{#if mode == "landing"}
    <header
        class="sticky top-0 z-10 flex h-[80px] items-center justify-center transition-all duration-300 ease-in-out"
        class:bg-base-100={!scrollToTop}
        class:shadow-lg={!scrollToTop}
    >
        <div class="container flex items-center">
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
            <nav class="flex gap-2">
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
