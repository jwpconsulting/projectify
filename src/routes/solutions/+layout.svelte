<script lang="ts">
    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
</script>

<PageLayout headerMode={"landing"}>
    <main class="page bg-base-100">
        <slot />
    </main>
</PageLayout>
