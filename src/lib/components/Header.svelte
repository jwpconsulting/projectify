<script lang="ts">
    import { page } from "$app/stores";
    import { user, logout } from "$lib/stores/user";
    import routes from "$lib/routes";

    $: userData = $user;
    $: items = [
        ...routes,
        { label: "Signout", action: logout, authRequired: true },
    ].filter((it) => {
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

<header class="h-16 bg-gray-200 flex items-center p-4">
    <nav>
        <ul class="flex">
            {#each items as it}
                <li class:active={$page.url.pathname === it.to}>
                    <a
                        on:click={it.action}
                        class="p-2 cursor-pointer"
                        href={it.to}
                    >
                        {it.label}
                    </a>
                </li>
            {/each}
        </ul>
    </nav>
    {#if userData}
        <div>{userData?.email}</div>
    {/if}
</header>
