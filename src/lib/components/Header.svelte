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

        if (!userData && it.authRequired === true) {
            return false;
        }

        if (userData && it.authRequired === false) {
            return false;
        }

        return true;
    });
</script>

<header class="h-[80px] flex items-center p-4 border-b border-base-300">
    <a href="/" class="flex mr-8">
        <HeaderLogo />
    </a>
    <nav class="grow">
        <ul class="flex">
            {#each items as it}
                <li class:active={$page.url.pathname === it.to}>
                    <a
                        on:click={it.action}
                        class="p-2 cursor-pointer font-bold"
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
