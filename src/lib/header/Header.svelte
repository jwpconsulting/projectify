<script lang="ts">
    import { page } from "$app/stores";
</script>

<header>
    <nav>
        <ul>
            <li class:active={$page.path === "/"}>
                <a sveltekit:prefetch href="/">Home</a>
            </li>
        </ul>
    </nav>
</header>
