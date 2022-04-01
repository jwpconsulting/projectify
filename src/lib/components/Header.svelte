<script lang="ts">
    import { page } from "$app/stores";
    import { user, logout } from "$lib/stores/user";
    import routes from "$lib/routes";
    import { _ } from "svelte-i18n";
    import HeaderLogo from "./assets/headerLogo.svelte";
    import HeaderUser from "./headerUser.svelte";

    $: userData = $user;
    $: items = [...routes].filter((it) => {
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
</script>

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
