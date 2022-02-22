<script lang="ts">
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import { _ } from "svelte-i18n";
</script>

<PageLayout>
    <main class="page page-center">
        <h1>{$_("home", { default: "Home" })}</h1>
    </main>
</PageLayout>
