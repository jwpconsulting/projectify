<script lang="ts">
    import { page } from "$app/stores";

    const items = [
        { label: "Home", to: "/" },
        { label: "Signin", to: "/signin" }
    ];
</script>

<header class="h-16 bg-gray-200 flex items-center p-4">
    <nav>
        <ul class="flex">
            {#each items as it}
                <li class:active={$page.path === it.to}>
                    <a class="p-2" sveltekit:prefetch href={it.to}
                        >{it.label}</a
                    >
                </li>
            {/each}
        </ul>
    </nav>
</header>
