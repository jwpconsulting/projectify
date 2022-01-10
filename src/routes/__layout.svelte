<script lang="ts">
    import "../app.scss";
    import Header from "$lib/components/Header.svelte";
    import "../i18n.js";
</script>

<Header>
    <main class="flex">
        <slot />
    </main>
</Header>
<slot />
