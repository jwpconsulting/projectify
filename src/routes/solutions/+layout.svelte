<script lang="ts">
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
    import { _ } from "svelte-i18n";
</script>

<PageLayout headerMode={"landing"}>
    <main class="page bg-base-100">
        <slot />
    </main>
</PageLayout>
