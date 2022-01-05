<script lang="ts">
    import { page } from "$app/stores";
    import { user, logout } from "$lib/stores/user";

    $: userData = $user;
    $: items = [
        { label: "Home", to: "/" },
        { label: "Signin", to: "/signin", authRequired: false },
        { label: "Signout", action: logout, authRequired: true }
    ].filter((it) => {
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
                <li class:active={$page.path === it.to}>
                    <a
                        on:click={it.action}
                        class="p-2"
                        sveltekit:prefetch
                        href={it.to}
                    >
                        {it.label}
                    </a>
                </li>
            {/each}
        </ul>
    </nav>
</header>
