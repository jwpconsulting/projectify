<script lang="ts">
    import { page } from "$app/stores";
</script>

<header class="h-16 bg-gray-200 flex items-center p-4">
    <nav>
        <ul>
            <li class:active={$page.path === "/"}>
                <a sveltekit:prefetch href="/">Home</a>
            </li>
        </ul>
    </nav>
</header>
